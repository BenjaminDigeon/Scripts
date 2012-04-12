#!/usr/bin/python
# Script de conversion de fichier CSV
# en requete INSERT SQL
# Benjamin Digeon

import sys
import os
import csv
import getopt

#Le separateur du fichier CSV
SEPARATEUR = ';'

# Fonction qui prend en arguments :
# Le nom de la table SQL
# Une liste contenant les noms des champs
# Une liste de liste contenant les informations
# Et qui renvoi la requete SQL 
def create_requete_SQL(nom_table,liste_header,liste_contenu):
	requete = 'INSERT INTO '
	requete += nom_table
	requete +=" ("

	for indice, valeur in enumerate(liste_header):
		requete += valeur
		if(indice != len(liste_header)-1):
			requete += ','
	
	requete +=")"
	requete +=" VALUES "
	
	for indice_g, valeur_g in enumerate(liste_contenu):
		requete+="("
		for indice,valeur in enumerate(valeur_g):		
			try:
				tmp = int(valeur)
				requete+=valeur
			except:
				requete+="'"
				requete+=valeur
				requete+="'"	
			if(indice != len(valeur_g)-1):
				requete += ','
		requete+=")"
		if(indice_g != len(liste_contenu)-1):
			requete += ','

	requete +=" ;"
	return requete

# Fonction qui prend en arguments :
# Le nom du fichier csv contenant les informations
# Et qui renvoi la requete SQL
def create_requete(nom_fichier):
	
	nom_table = '.'.join(nom_fichier.split('.')[:-1])
	
	csv_reader = csv.reader(open(nom_fichier,"rU"),delimiter=SEPARATEUR,quotechar='|')
	
	liste_header = []
	liste_contenu = []
	
	for row in csv_reader:
		if(csv_reader.line_num==1):
			liste_header = row
		else:
			liste_contenu.append(row)
	
	return create_requete_SQL(nom_table,liste_header,liste_contenu)

# Fonction principale qui prend une serie de .csv en argument
# Et ecrit les requetes SQL correspondante dans un fichier .sql
# Par defaut requete.sql mais specifiable avec l'option -o
def main(argv):
	
	nom_fichier = "requete.sql"
	try:
		opts, args = getopt.getopt(argv, "ho:", ["help"])
		
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()

		elif opt == 'o':
			nom_fichier = arg
	
	if(len(args)<1):
		usage()
		sys.exit()
	
	fichier = open(nom_fichier,"a")
	
	for nom_fichier_in in args:
		fichier.write(create_requete(nom_fichier_in))
		fichier.write("\n")
	
	fichier.close()
		
def usage():
	print "Usage :",sys.argv[0]," [-o fichier.sql] [-h --help] fichier1.cvs ..."

if __name__ == '__main__':
	main(sys.argv[1:])
