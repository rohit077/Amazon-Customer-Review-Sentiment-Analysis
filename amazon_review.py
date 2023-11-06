from requests_html import HTMLSession
import json
import time

class reviews:
    def __init__(self, asin) -> None:
        self.session = HTMLSession()
        self.asin = asin
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}
        self.url = f'https://www.amazon.in/Apple-MacBook-Chip-13-inch-256GB/product-reviews/B08N5W4NNB/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'

    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        if not r.html.find('div[data-hook=review]'):
            return False
        else:
            return r.html.find('div[data-hook=review]')
            
        
    def parse(self, reviews):
        if not reviews:
            print("No reviews found.")
            return []

        total = []
        for review in reviews:
            body = review.find('span[data-hook=review-body] span', first=True).text.replace('\n', '').strip()

            data = {
                'body': body[:100]
            }
            total.append(data)
        return total
    
    def save(self, results):
        with open(self.asin + 'reviews.json', 'w') as f:
            json.dump(results, f)


#if __name__ == '__main__':
#    asin = 'RCPJX01GN6HBG'
#    amazon_review = reviews(asin)
#    reviews = amazon_review.pagination(1)
#    print(amazon_review.parse(reviews))


if __name__ == '__main__':
    asin = 'R1SA1ULL7M4XZO'
    amazon_review = reviews(asin)
    results = []
    for x in range(1, 5):
        print('Review', x)
        time.sleep(0.5)
        reviews = amazon_review.pagination(x)
        if reviews is not False:
            results.append(amazon_review.parse(reviews))
        else:
            print('No more pages')
            break

    amazon_review.save(results)