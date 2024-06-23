import threading

thread_local = threading.local()


class SubscriptionDeletionContext:
    def __enter__(self):
        thread_local.subscription_deleting = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        thread_local.subscription_deleting = False


class BranchDeletionContext:
    def __enter__(self):
        thread_local.branch_deleting = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        thread_local.branch_deleting = False
