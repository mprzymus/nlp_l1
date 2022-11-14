import datetime as dt
import json
import typing as t
from dataclasses import dataclass, field, replace

import pandas as pd
import snscrape.modules.twitter as twt
from tqdm import tqdm

from config import SCRAPED_DIR, SCRAPED_DONE, date_range

TWEETS_DIR = SCRAPED_DIR / dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
TWEETS_DIR.mkdir(exist_ok=True, parents=True)

MIN_LEN = 40
MAX_RESULTS = 1_000


def read_done() -> set[str]:
    done = json.loads(SCRAPED_DONE.read_text()) if SCRAPED_DONE.is_file() else []
    return set(done)


@dataclass
class SearchQuery:
    args: set[str] = field(default_factory=set)

    def user(self, name: str) -> "SearchQuery":
        return replace(self, args=self.args | {f"from:{name}"})

    def hashtag(self, hashtag: str) -> "SearchQuery":
        return replace(self, args=self.args | {f"#{hashtag}"})

    def language(self, language: str) -> "SearchQuery":
        return replace(self, args=self.args | {f"lang:{language}"})

    def from_(self, date: dt.date):
        return replace(self, args=self.args | {f"since:{date.isoformat()}"})

    def to(self, date: dt.date) -> "SearchQuery":
        # Twitter's 'until' is actually 'before'
        corrected = date + dt.timedelta(days=1)
        return replace(self, args=self.args | {f"until:{corrected.isoformat()}"})

    def __str__(self) -> str:
        return " ".join(sorted(self.args))


@dataclass
class Scraper:
    done: set[str] = field(default_factory=read_done)

    def scrape(
        self,
        language: str,
        from_: dt.date,
        to: dt.date,
        user: t.Optional[str] = None,
        hashtag: t.Optional[str] = None,
        scrape_replies: bool = False,
    ) -> None:
        if from_.isoformat() in self.done:
            return

        query = SearchQuery().language(language).from_(from_).to(to)

        if hashtag:
            query = query.hashtag(hashtag)

        if user:
            query = query.user(user)

        scraper = twt.TwitterSearchScraper(str(query))
        tweets: list[twt.Tweet] = []
        for tweet in scraper.get_items():
            if len(tweet.content) > 40:
                tweets.append(tweet)

                if len(tweets) >= MAX_RESULTS:
                    break

        if scrape_replies:
            tweet_ids = [tweet.id for tweet in tweets if tweet.replyCount > 0]

            for tweet_id in tweet_ids:
                replies_scraper = twt.TwitterTweetScraper(
                    tweet_id,
                    mode=twt.TwitterTweetScraperMode.SCROLL,
                )
                tweets.extend(replies_scraper.get_items())

        self.save_tweets(tweets, of_date=from_, replies=scrape_replies)

    def save_tweets(self, tweets: list[twt.Tweet], of_date: dt.date, replies: bool):
        if not tweets:
            return

        df = pd.DataFrame([self.tweet_to_dict(tweet) for tweet in tweets])
        df.drop_duplicates(subset="id")
        df["replies_scraped"] = replies
        as_json = df.to_json(orient="records", lines=True)

        output_file = TWEETS_DIR / f"{of_date.isoformat()}.jsonl"
        with output_file.open("a") as f:
            f.write(as_json)

        self.done.add(of_date.isoformat())
        done = list(self.done)
        done.sort()
        SCRAPED_DONE.write_text(json.dumps(done, indent=2))

    @staticmethod
    def tweet_to_dict(tweet: twt.Tweet) -> dict:
        return dict(
            id=tweet.id,
            content=tweet.content,
            username=tweet.user.username,
            timestamp=tweet.date,
            replies=tweet.replyCount,
            quoted=tweet.quotedTweet.id if tweet.quotedTweet else 0,
            reply_to=tweet.inReplyToTweetId if tweet.inReplyToTweetId else 0,
            hashtags=tweet.hashtags if tweet.hashtags else [],
        )


def main():
    scraper = Scraper()

    for date in tqdm(date_range()):
        scraper.scrape(
            language="pl",
            from_=date,
            to=date,
            scrape_replies=False,
        )


if __name__ == "__main__":
    main()
