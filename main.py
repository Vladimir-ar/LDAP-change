import getpass
from ldap3 import *
import sqlite3

# Работаем с БД.
db_conn = sqlite3.connect('Input_db.sqlite')
db_cursor = db_conn.cursor()
select1 = db_cursor.execute("SELECT * FROM UserHostname")
print(select1.fetchall())

# Создаем Словарь aDict, в котором: Login => HOSTNAME
newList =[]
for row in db_cursor.execute("SELECT * FROM UserHostname"):
    newList.append(row)
#print((newList[0])[1])

aDict_keys = []
aDict_values = []
for i in range(len(newList)):
    aDict_keys.append((newList[i])[0])
    aDict_values.append(((newList[i])[1]))

aDict = dict(zip(aDict_keys,aDict_values))
print("Key-value: "+ str(aDict))

#
# server = Server(str(ldap_server_address), get_info=ALL, port=389)
#         # ldap_conn = Connection(server, 'cn=ivanov,ou=Container1_users,dc=myown,dc=local', str(password))
# ldap_conn = Connection(server, user=str(username), password=str(password_input))
# ldap_conn.bind()
# for login, hostname in aDict.items():
#     ldap_conn.search('dc=myown,dc=local', '(&(objectCategory=person)(memberOf=cn=Group1,dc=myown,dc=local))')
#     if login[:-3] in ldap_conn.entries:
#         print("YES True")
#         print(login[:-3], ldap_conn.entries)
#     else:
#         print("No, False")
#         print(login[:-3], ldap_conn.entries)




ldap_server_address = input("Enter LDAP server address or FQDN: \n")
username = input("Enter username: \n")
password_input = getpass.getpass(prompt='Password: ')



def reconnect():
    ldap_server_address = input("Enter LDAP server address or FQDN: \n")
    username = input("Enter username: \n")
    password_input = input("Enter password: \n")
    return authenticate(ldap_server_address, username, password_input)

def authenticate(ldap_server_address, username, password_input):
    try:
        server = Server(str(ldap_server_address), get_info=ALL, port=389)
        # ldap_conn = Connection(server, 'cn=ivanov,ou=Container1_users,dc=myown,dc=local', str(password))
        ldap_conn = Connection(server, user=str(username), password=str(password_input))
        ldap_conn.bind()
        assert not ldap_conn.extend.standard.who_am_i() == None, 'authenticate ERROR'
    except AssertionError:
        print('authenticate ERROR. Try again')
        ldap_conn.closed
        reconnect()
    except LDAPSocketOpenError:
        print('LDAPSocketOpenError. Try again')
        ldap_conn.closed
        reconnect()
    else:
        print('Connect successful')
        print('Connected to '+str(ldap_server_address)+' as '+str(ldap_conn.extend.standard.who_am_i()))
        print('General info: '+ str(ldap_conn))
    # print(server.info)
    # ldap_conn.search('dc=myown,dc=local', '(objectCategory=person)')


#
#     ldap_conn.search('dc=myown,dc=local', '(&(objectCategory=person)(memberOf=cn=Group1,dc=myown,dc=local))')
#     print(ldap_conn.entries)
#     login = 'petrov.aa'
#     ldap_conn.search('dc=myown,dc=local', '(sAMAccountName=%s)' % login)
#     print(ldap_conn.entries)

    # Show all groups
    # ldap_conn.search('dc=myown,dc=local', '(objectCategory=group)')
    # print(ldap_conn.entries)

    group = input("Enter AD_Group to search and change: \n")
    def modify_ldap(group):
    # '''Если юзер в группе А, то переместить связанную с ним учетку компьютера в группу В.
    # Uername => hostname в словаре aDict берутся из Базы Данных Input_db.sqlite
    # '''

        for login, hostname in aDict.items():
            ldap_conn.search('dc=myown,dc=local', '(&(memberOf=cn=%s,dc=myown,dc=local)(sAMAccountName=%s))' % (group, login))

     # ldap_conn.search('dc=myown,dc=local', '(&(sAMAccountName=petrov.aa)(memberOf=cn=Group1,dc=myown,dc=local))')
            if ldap_conn.entries != []:
                ldap_conn.modify_dn('cn=%s,ou=Container3_computers,dc=myown,dc=local'% hostname, 'cn=%s'% hostname, new_superior='ou=Container4_computers,dc=myown,dc=local')

                print("%s was moved" % hostname)

#conn.modify_dn('cn=pc-1,ou=Container3_computers,dc=myown,dc=local', 'cn=pc-1', new_superior='ou=Container4_computers,dc=myown,dc=local')
    modify_ldap(group)

authenticate(ldap_server_address, username, password_input)

#-----






