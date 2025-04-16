
def Calculer_le_masque(n_hotes):

    # calcule de  masque et hôtes nécessaires et la taille de reseau et le nomber n ex 2 a la puissance  n
    for n in range(1, 33):
        if (2 ** n - 2) >= n_hotes:
            break

    masque = 32 - n
    taille_reseau = 2 ** n
    host = taille_reseau - 2 

    return masque, taille_reseau, host 


def increment_ip(ip, increment):
    Octet_list = list(map(int, ip.split('.')))

    # Ajouter l'incrément au dernier octet
    Octet_list[3] += increment
    
    # Propager les retenues aux octets supérieurs                             #192.168.1.250 + 300 = 192.168.3.38
    for i in range(3, 0, -1):                                                 #250 + 300 = 550, dépasse 255 :                                                                  
        if Octet_list[i] > 255:                                                 # 550 // 256 = 2 → On ajoute 2 au troisième octet.
            Octet_list[i - 1] += Octet_list[i] // 256                             #550 % 256 = 38 → Nouveau dernier octet.
            Octet_list[i] = Octet_list[i] % 256
            
    # verifier si on dépasse la plage IP valide
    if Octet_list[0] > 255:
        raise ValueError ("l'increment a dépassé la plage d'IP")
          
    return '.'.join(map(str, Octet_list))


def calcul_vlsm(ip_debut, sous_reseaux):

    # Trier les sous-réseaux de la plus grande à la plus petite taille
    sous_reseaux.sort(reverse=True)

    
    ip_courante = ip_debut
    resultats = []
    
    for n_hotes in sous_reseaux:
        # Calcul du masque et du nombre d'hôtes nécessaires pour le sous-réseau
        masque, taille_reseau, host = Calculer_le_masque(n_hotes)
        
        # Ajouter l'adresse réseau et de diffusion
        adresse_reseau = ip_courante
        adresse_diffusion = increment_ip(adresse_reseau, taille_reseau -1 )
        premier_address = increment_ip(adresse_reseau, +1)
        dernier_address = increment_ip(adresse_diffusion, -1)
        
        # Ajouter les résultats à la liste
        resultats.append({
             'add':adresse_reseau,
             '/CIDR':f"/{masque}",
             'padd':premier_address,
             'dadd':dernier_address,
             'adddif':adresse_diffusion,
             'n_hotes':host,
        })
        
        # Incrémenter l'adresse IP pour le prochain sous-réseau
        ip_courante = increment_ip(adresse_diffusion, +1)
    
    return resultats
def filtrer_et_rectifier_ip(ip_debut, CIDR):                 
    octets = list(map(int, ip_debut.split('.')))
    #Vérifier si address ip depass 4 octets
    if len(octets)!=4:
        raise ValueError("adresse IPinvalide (>4 octtet)")
     # Vérifier si un octet dépasse 255
    for octet in octets :
        if octet > 255:
            raise ValueError("adresse IP invalide")
    bits_hote = 32 - CIDR
    # Filtres IP invalides
    if octets == [0, 0, 0, 0]:
        raise ValueError("adresse IP invalide")
    if octets == [255, 255, 255, 255]:
        raise ValueError("adresse IP invalide")
    if octets[0] == 127:
        raise ValueError("adresse IP invalide")
    if octets[0] == 169 and octets[1] == 254:
        raise ValueError("adresse IP invalide")
    if 224 <= octets[0] <= 239:
        raise ValueError("adresse IP invalide")
    if octets[0] == 100 and 64 <= octets[1] <= 127:
        raise ValueError("adresse IP invalide")
    if octets[0] == 198 and 18 <= octets[1] <= 19:
        raise ValueError("adresse IP invalide")
    if octets[0] == 192 and octets[1] == 0 and octets[2] == 2:
        raise ValueError("adresse IP invalide")
    if octets[0] == 198 and octets[1] == 51 and octets[2] == 100:
        raise ValueError("adresse IP invalide")
    if octets[0] == 203 and octets[1] == 0 and octets[2] == 113:
        raise ValueError("adresse IP invalide")
    if 240 <= octets[0] <= 255 and not (octets == [255,255,255,255]):
        raise ValueError("adresse IP invalide")

    # Rectification de la partie hôte
    for i in range(3, -1, -1):
        if bits_hote >= 8:
            octets[i] = 0
            bits_hote -= 8
        elif bits_hote > 0:
            bloc = 2 ** bits_hote
            octets[i] = (octets[i] // bloc) * bloc
            break

    return '.'.join(map(str, octets))
def verifier_sous_reseaux(sous_reseaux, CIDR):
    if not sous_reseaux:
        raise ValueError("Veuillez remplir les tailles des sous-réseaux.")

    if not (1 <= CIDR <= 30):
        raise ValueError("Le masque doit être entre 1 et 30")

    somme_des_hotes = sum(sous_reseaux)
    capacite = 2 ** (32 - CIDR)

    if somme_des_hotes > capacite:
        raise ValueError("La somme des hôtes dépasse la capacité disponible")
