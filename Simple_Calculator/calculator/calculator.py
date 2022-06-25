from celery import Celery

app = Celery('calculator', broker='pyamqp://guest:guest@localhost:5672', backend=f'redis://localhost:6379')

@app.task
def idx_palindrome_prime(idx):
        prime = 0
        result = 0
        num = 2

        while prime != idx:
            factor = 0
            for i in range(1, num + 1):
                if num % i == 0:
                    factor += 1  
            reverse = 0
            tmp = num
            while tmp != 0:
                left = tmp % 10
                reverse = reverse * 10 + left
                tmp = int(tmp / 10)

            if factor == 2 and reverse == num:
                prime += 1
                result = num

            num  += 1

        return result

@app.task
def idx_prime(idx):
        prime = 0
        result = 0
        num = 2
        while prime != idx:
            factor = 0
            for i in range(1, num + 1):
                if num % i == 0:
                    factor += 1

            if factor == 2:
                prime += 1
                result = num
            num  += 1

        return result
