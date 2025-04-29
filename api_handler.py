from requests import get

cat_api_url = 'https://cataas.com/cat?json=true'
dog_api_url = 'https://dog.ceo/api/breeds/image/random'
bird_api_url= 'https://api.unsplash.com/photos/random?client_id=_oED5ZIDWwfgdYKfSFKTH7_ceenn9Jpb9W3ykoeKGDA&query=bird'

class APIHandler:

    @staticmethod
    def get_rand_cat() -> tuple[bytes, str] | None:
        res = get(cat_api_url)

        if res.status_code != 200: return
        
        img_res = get(res.json()['url'])

        if img_res.status_code != 200: return

        return img_res.content, img_res.url


    @staticmethod
    def get_rand_dog() -> tuple[bytes, str] | None:
        res = get(dog_api_url)

        if res.status_code != 200: return

        img_res = get(res.json()['message'])

        if img_res.status_code != 200: return

        return img_res.content, img_res.url


    @staticmethod
    def get_rand_bird() -> tuple[bytes, str] | None:
        res = get(bird_api_url)

        if res.status_code != 200: return

        img_res = get(res.json()['urls']['small'])

        if img_res.status_code != 200: return

        return img_res.content, img_res.url