import requests


original = open("wp-conf.txt", "r")
tmp = open("wp-tmp.txt", "w")

# Debug data
db_name = "wp-db"
db_user = "wp-admin"
db_passwd = "wp-passwd"

url = 'https://api.wordpress.org/secret-key/1.1/salt/'
response = requests.get(url)
salts = response.text.splitlines(True)

if response.status_code != 200:
    print("[WARNING] An error occurred: ", response.status_code)
    print("[INFO] Skipping writing SALT")
    for line in original.readlines():
        match line.strip():
            case "define( 'DB_NAME', 'database_name_here' );":
                tmp.write(f"define( 'DB_NAME', '{db_name}' );")
            case "define( 'DB_USER', 'username_here' );":
                tmp.write(f"define( 'DB_USER', '{db_user}' );")
            case "define( 'DB_PASSWORD', 'password_here' );":
                tmp.write(f"define( 'DB_PASSWORD', '{db_passwd}' );")
            case other:
                tmp.write(line)
    tmp.close()
    original.close()
        
    #TODO: Write tmp into original
    exit()


for line in original.readlines():
    match line.strip():
        case "define( 'DB_NAME', 'database_name_here' );":
            tmp.write(f"define( 'DB_NAME', '{db_name}' );")
        case "define( 'DB_USER', 'username_here' );":
            tmp.write(f"define( 'DB_USER', '{db_user}' );")
        case "define( 'DB_PASSWORD', 'password_here' );":
            tmp.write(f"define( 'DB_PASSWORD', '{db_passwd}' );")
        case "define( 'AUTH_KEY',         'put your unique phrase here' );":
            tmp.write(salts[0])
        case "define( 'SECURE_AUTH_KEY',  'put your unique phrase here' );":
            tmp.write(salts[1])
        case "define( 'LOGGED_IN_KEY',    'put your unique phrase here' );":
            tmp.write(salts[2])
        case "define( 'NONCE_KEY',        'put your unique phrase here' );":
            tmp.write(salts[3])
        case "define( 'AUTH_SALT',        'put your unique phrase here' );":
            tmp.write(salts[4])
        case "define( 'SECURE_AUTH_SALT', 'put your unique phrase here' );":
            tmp.write(salts[5])
        case "define( 'LOGGED_IN_SALT',   'put your unique phrase here' );":
            tmp.write(salts[6])
        case "define( 'NONCE_SALT',       'put your unique phrase here' );":
            tmp.write(salts[7])
        case other:
            tmp.write(line)

tmp.close()
original.close()

#TODO: Write tmp into original

