from datetime import datetime, timedelta


class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return f'Bucket(quota={self.quota})'


def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


def deduct(bucket,amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False # Bucket hasn't been filled this period
    if bucket.quota - amount < 0:
        return False # Bucket was filled but not enough
    bucket.quota -= amount
    return True # Bucket had enough, quota consumed

def takeout(bucket, amount):
    if deduct(bucket, amount):
        print(f"Had {amount} quota")
    else:
        print(f"Not enough for {amount} quota")


print("First Bucket: timedelta=60, quota=100")
bucket = Bucket(60)
fill(bucket, 100)
print(bucket)
print("First Takeout 99")
takeout(bucket, 99)
print("Second Takeout 3")
takeout(bucket, 3)


class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (f"NewBucket(max_quota={self.max_quota}, quota_consumed={self.quota_consumed})")

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # Quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


print("Second Bucket <NewBucket>: timedelta=60, quota=100")
bucket = NewBucket(60)
print("Initial", bucket)
fill(bucket, 100)
print("Filled", bucket)
takeout(bucket, 99)
print("Now", bucket)
takeout(bucket, 3)
print("Still", bucket)
