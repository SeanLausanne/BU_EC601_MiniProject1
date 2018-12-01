import twitter_imgs_mysql as ms
import twitter_imgs_MongoDB as mg

db = input('Please select: 1.MySQl, 2.MongoDB\n')

if db not in ['1', '2']:
    print('Invalide input')

else:
    operate = input('Please select:\n1.Add an account\n2.Query an account\n'
                    '3.Delete_an_account\n4.Seach a label\n5.Get general info\n')

    if operate not in ['1','2','3','4','5']:
        print('Invalide input')

    else:
        operate = int(operate)
        db = int(db)

        if db == 1:
            cursor = ms.connect_MySQL()

        if operate == 1:
            if db == 1:
                ms.add_account(cursor)
            else:
                mg.add_account()

        elif operate == 2:
            if db == 1:
                ms.query_account(cursor)
            else:
                mg.query_account()

        elif operate == 3:
            if db == 1:
                ms.delete_account(cursor)
            else:
                mg.delete_account()

        elif operate == 4:
            if db == 1:
                ms.search_label(cursor)
            else:
                mg.search_label()

        else:
            if db == 1:
                ms.get_all_and_most_common(cursor)
            else:
                mg.get_all_and_most_common()