import getpass
import bcrypt

password = getpass.getpass("Inserisci la password admin: ")
hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
print(hashed.decode("utf-8"))