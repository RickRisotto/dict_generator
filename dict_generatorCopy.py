#!/usr/bin/env python
# -*- coding: utf-8 -*-



""" This module creates an example of book with arbitrary properties"""


def subgen():
    ''' Creates a dict which will be nested to main dict as a value'''
    
    from RandomWordGenerator import RandomWord
    import random
    import datetime

    year = str(datetime.datetime.now() - datetime.timedelta(days=random.randrange(400, 1000)))[0:4]
    isbn_13 =  '{}-{}-{}-{}-{}'.format(random.randrange(111, 999), random.randrange(1, 10),
                                        random.randrange(0, 99999),
                                        random.randrange(111, 999),
                                        random.randrange(1, 10)
                                        )
    rw = RandomWord(max_word_size=5)
    book_name = rw.generate()
    res = str(int(random.random()))

    author = (((lambda x, y: x+y)(("author_{}, ".format(random.randrange(101, 200))),
                                    ("author_{}".format(random.randrange(1, 100)))))).split(',')
    rating = random.randrange(1, 100)
    price = round(random.uniform(1111111.0, 999999.9),2)
    discount = random.randrange(1, 50)
    val_for_nested_dict = ['{}_book'.format(book_name), year, (str(random.randrange(50, 1500))),isbn_13, rating,
                                price, discount]
    lst_for_nested_dict = ["title","year", "pages", "isbn13", "rating", "price", "discount", "author"]
    nested_dict = ','.join(('{},{}'.format(y,x) for y, x in (list(i for i in (zip(lst_for_nested_dict,
                                                                                  val_for_nested_dict)))))).split(',')
    final = {"author": author}
    i = iter(nested_dict)
    ndict = dict(zip(i, i))
    #ndict.update(final)
    #res = {}
    while True:
        item = yield
        if item is None:
            break
        ndict.update(final)
    return ndict

def delegate(result, key):
    while True:
        result[key] = yield from subgen()

def main_gen():
    import pprint
    import random
    from RandomWordGenerator import RandomWord

    rw = RandomWord(max_word_size=5)
    for_model = rw.generate()
    res = str(int(random.random()))
    model = "shop_{}.book".format(for_model)
    result = {}
    #for_result_dict = next(subgen())
    #result.update(for_result_dict)
    val = [model, random.randrange(1, 50)]
    keys = ["model", "pk"]
    final = ','.join(('{},{}'.format(y, x) for y, x in (list(i for i in (zip(keys, val)))))).split(',')
    fld = {"field": ' '}
    for key, val in fld.items():
        collect = delegate(result, key)
        next(collect)
        for v in val:
            collect.send(v)
        collect.send(None)


    i = iter(final)
    book = dict(zip(i, i))
    book.update(result)

    while True:
        yield book


if __name__ == "__main__":
    main_gen = main_gen()
    pprint.pprint(next(main_gen))
