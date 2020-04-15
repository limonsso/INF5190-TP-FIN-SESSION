CREATE TABLE "inspections" (
	"id"	TEXT NOT NULL,
	"proprietaire"	TEXT NOT NULL,
	"categorie"	TEXT NOT NULL,
	"etablissement"	TEXT NOT NULL,
	"adresse"	TEXT NOT NULL,
	"ville"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"date_infraction"	TEXT NOT NULL,
	"date_jugement"	TEXT NOT NULL,
	"montant"	TEXT NOT NULL,
	PRIMARY KEY("id")
)

CREATE TABLE "contrevenants" (
	"id"	TEXT NOT NULL,
	"proprietaire"	TEXT NOT NULL,
	"categorie"	TEXT NOT NULL,
	"etablissement"	TEXT NOT NULL,
	"adresse"	TEXT NOT NULL,
	"ville"	TEXT NOT NULL,
	"has_been_deleted"	INTEGER DEFAULT 0,
	PRIMARY KEY("id")
)

CREATE TABLE "infractions" (
    "id"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"date_infraction"	TEXT NOT NULL,
	"date_jugement"	TEXT NOT NULL,
	"montant"	TEXT NOT NULL,
	"contrevenant_id"	TEXT NOT NULL,
	"inspection_id"	TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY (contrevenant_id) REFERENCES contrevenants(id),
	FOREIGN KEY (inspection_id) REFERENCES inspections(id)
)

CREATE TABLE "users" (
    "id"	TEXT NOT NULL,
    "username"	TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "etablissements" TEXT NOT NULL,
    "password_hash" TEXT NOT NULL,
    "salt" TEXT NOT NULL,
    "avatar" BLOB NOT NULL
    PRIMARY KEY("id")
)

CREATE TABLE "user_contrevenants" (
    "user_id"	TEXT NOT NULL,
    "contrevenant_id"	TEXT NOT NULL,
    PRIMARY KEY("user_id","contrevenant_id"),
	FOREIGN KEY (contrevenant_id) REFERENCES contrevenants(id),
	FOREIGN KEY (user_id) REFERENCES users(id)
)

CREATE TABLE sessions (
    "id" TEXT PRIMARY KEY,
    "user_id" TEXT,
    FOREIGN KEY(user_id) references users(id)
);