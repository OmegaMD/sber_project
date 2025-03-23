# user class
class User:
    # class initialization function
    def __init__(self, id, last_used_partners):
        self.id = id                                  # user identifier probably a string
        self.last_used_partners = last_used_partners  # list of 10 or less last used partners

# partner class
class Partner:
    # class initialization funciton
    def __init__(self, type, name, site_link, image_url, logo_url):
        self.type = type              # types: "кондитерская", "магазин", "аптека" и т.д.
        self.name = name              # just partner company name
        self.site_link = site_link    # link to partners website
        self.image_url = image_url    # link to main page image
        self.logo_url = logo_url      # link to partner's logo image

# database class
class Database:
    # class initialization function
    def __init__(self, filename):
        self.filename = filename # file directory where database is being stored

    # user info accessing function
    def access_user(self, id):
        return User(id, [Partner("кондитерская", "Буше", "site link", "https://avatars.mds.yandex.net/get-altay/4377463/2a00000182500a731822c9b8459bae41d2ab/L_height", "https://s.rbk.ru/v1_companies_s3/media/trademarks/1a677d0a-a614-4a7f-b77b-66d9d32a9d01.jpg")])

    # partner by name accessing function
    def access_partner(self, name):
        return Partner("аптека", name, "site link", "https://avatars.mds.yandex.net/get-altay/4377463/2a00000182500a731822c9b8459bae41d2ab/L_height", "https://s.rbk.ru/v1_companies_s3/media/trademarks/1a677d0a-a614-4a7f-b77b-66d9d32a9d01.jpg")

    # top 10 partners with the best discounts accessing function
    def access_top_discount_partners(self):
        return [Partner("кафе", "Буше", "site link", "https://avatars.mds.yandex.net/get-altay/4377463/2a00000182500a731822c9b8459bae41d2ab/L_height", "https://s.rbk.ru/v1_companies_s3/media/trademarks/1a677d0a-a614-4a7f-b77b-66d9d32a9d01.jpg") for _ in range(10)]