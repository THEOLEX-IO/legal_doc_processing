Etapes:

- Comprendre les aspects fonctionnels, les données et les bénéfices d'une telle démarche d'extraction d'informations.  
- Une phase de bibliographie sera nécessaire afin de capitaliser sur l'état de l'art actuel en termes d'extraction de données.  
- Il y aura tout d'abord un travail de cleaning et de reconstruction du texte extrait des documents grâce à l'OCR.  
- Il est demandé de faire une segmentation de ces documents afin de reconstruire les sections importantes et redondantes dans les documents traités. Ce travail facilitera la phase d'extraction d'information. Il est possible de s'appuyer sur des algorithmes de classification pour cette étape.  
- Tester plusieurs méthodes d'extraction de données et établir des indicateurs de performances (précision, recall...)   
- Mettre en place des tests unitaires de couverture sur quelques documents types.  
- Faire un focus en particulier sur les transformers par le biais de huggingface. Ces algorithmes présentent des méthodes très avancées qui pourraient résoudre quelques cas d'usage. QA, entailement, ZSL, NER...  
- Nous allons commencer par une dizaine de champs qui vous seront transmis en même temps que les données.  
- Il faudra également commencer à réfléchir à des propositions de représentation des données et d'outil de tagging ou de rectification des résultats de la machine. L'équipe de développement et d'ux vous accompagnera sur ce sujet.  
- Dans un deuxième temps et après des résultats satisfaisants, vous allez participer avec l'équipe de développement à l'intégration de votre package dans les pipes de traitement quotidien  

Méthodologie tout au long du projet:

- L'équipe suit un workflow de travail structuré qui permet de progresser en autonomie et de notifier l'équipe en cas de blocage. Il faudra respecter ce processus pour réussir son intégration dans l'équipe.  
- Il faudrait respecter les standards de développement python (DRY, PEP8).  
- Mettre en place un package python qui contient tous les traitements développés.  
- Documentation détaillée du package et mise en place de notebooks/colab de démonstration.  
- Les inputs/output des différentes étapes doivent suivre les standards du NLP et du traitement de données. Format Json, conservation des métadonnées aussi bien pour les documents que pour les informations extraites.
