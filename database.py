# user class
class User:
    # class initialization function
    def __init__(self, id, last_used_partners):
        self.id = id                                  # user identifier probably a string
        self.last_used_partners = last_used_partners  # list of 10 or less last used partners

# partner class
class Partner:
    # class initialization funciton
    def __init__(self, type, name, site_link, image_url):
        self.type = type              # types: "кондитерская", "магазин", "аптека" и т.д.
        self.name = name              # just partner company name
        self.site_link = site_link    # link to partners website
        self.image_url = image_url  # link to main page image

# database class
class Database:
    # class initialization function
    def __init__(self, filename):
        self.filename = filename # file directory where database is being stored

    # user info accessing function
    def access_user(self, id):
        return User(id, [Partner("кондитерская", "Буше", "site link", "image link")])

    # partner by name accessing function
    def access_partner(self, name):
        return Partner("аптека", name, "site link", "image link")

    # top 10 partners with the best discounts accessing function
    def access_top_discount_partners(self):
        return [Partner("кондитерская", "Буше", "site link", "image link") for _ in range(10)]