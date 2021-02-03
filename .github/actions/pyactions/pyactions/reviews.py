import itertools

from ghapi.page import paged

from .actions import Logger


_log = Logger()


class ReviewState:
    approved = 'APPROVED'
    dismissed = 'DISMISSED'
    commented = 'COMMENTED'
    changes_requested = 'CHANGES_REQUESTED'
    affecting_approval = {
        approved,
        dismissed,
        changes_requested,
    }


def get_reviews(api, pr=None):
    params = dict(pull_number=pr.number) if pr is not None else {}
    for page_idx, page in enumerate(paged(api.pulls.list_reviews, **params)):
        _log.info(f'Fetching reviews: {page_idx=}, {len(page)=}')
        for review_in_page_idx, review in enumerate(page):
            _log.display(f'Review {review_in_page_idx}', review)
            yield review


class PullReviews:
    "Overall status of reviews for a PR."

    @classmethod
    def fetch(cls, api, pr=None, protected_branch_name='main'):

        _log.info(f'Fetching reviews')
        reviews = list(get_reviews(api, pr=pr))
        _log.info(f'Fetching branch protection rules ({protected_branch_name=})')
        branch_protection = api.repos.get_branch_protection(branch=protected_branch_name)

        return cls(
            pr=pr, 
            reviews=reviews,
            branch_protection=branch_protection,
        )

    def __init__(self,
            pr,
            reviews=None,
            branch_protection=None,
        ):
        self._pr = pr
        self._reviews = reviews or []
        self._branch_protection = branch_protection

    def __iter__(self):
        return iter(self._reviews)

    @property
    def by_user(self):
        def get_author(review):
            return review.author.login

        gb_key_items_pairs = itertools.groupby(self, key=get_author)
        return {
            author: list(reviews)
            for author, reviews in gb_key_items_pairs
        }

    @property
    def latest_by_user(self):
        by_user = {}
        for review in self:
            if review.state not in ReviewState.affecting_approval:
                continue
            by_user[review.user.login] = review

        return by_user

    @property
    def affecting_approval(self):
        return list(self.latest_by_user.values())

    @property
    def count_approved(self):
        approved = [
            r for r in self.affecting_approval
            if r.state == ReviewState.approved
        ]
        return len(approved)

    @property
    def required_count_approved(self):
        return (
            self._branch_protection
            .required_pull_request_reviews
            .required_approving_review_count
        )

    @property
    def is_status_approved(self):
        needs = self.required_count_approved
        has = self.count_approved
        is_approved = has >= needs

        _log.info(f'{needs=}, {has=}: {is_approved=}')

        return is_approved
