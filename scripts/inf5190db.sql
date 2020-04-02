CREATE TABLE "contrevenants" (
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
	"has_been_deleted"	INTEGER NOT NULL,
	"is_local_data"	INTEGER NOT NULL,
	"modification_date"	TEXT NOT NULL,
	"creation_date"	TEXT NOT NULL,
	PRIMARY KEY("id")
)