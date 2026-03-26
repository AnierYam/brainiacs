from __future__ import annotations

from typing import Any


SITE_LANGUAGE_COOKIE = "site_lang"
SUPPORTED_SITE_LANGUAGES = ("en", "fr")
DEFAULT_SITE_LANGUAGE = "en"


SITE_COPY: dict[str, dict[str, Any]] = {
    "en": {
        "common": {
            "brand_display": "BRAINIACS ACADEMY",
            "brand_meta": "Brainiacs Academy",
            "buy_kit": "Buy Kit",
            "contact_us": "Contact Us",
            "log_in": "Log In",
            "activate_kit": "Activate Kit",
            "open_navigation": "Open navigation",
            "language_switch": "Language switch",
            "back_to_home": "Back to Home",
            "footer_copyright": "2025 Brainiacs Academy. All rights reserved.",
            "show_password": "Show password",
            "hide_password": "Hide password",
            "toggle_password": "Toggle password visibility",
            "username": "Username",
            "password": "Password",
            "confirm_password": "Confirm Password",
            "activation_code": "Activation Code",
            "your_email": "Your Email",
            "verification_code": "Verification code",
        },
        "home": {
            "meta_title": "Brainiacs Academy",
            "hero_image_alt": "Robot building kit",
            "hero_title": "Robotics Made Simple",
            "hero_description": "Our interactive robot kits turn curious minds into confident builders",
            "hero_cta": "Learn How",
            "mission_title": "Our Mission",
            "mission_lead": "Brainiacs was built on one belief:",
            "mission_highlight": "With the right tools, learning robotics isn't hard.",
            "mission_text": "We make it clear, hands-on, and fun, with just the right level of challenge.",
            "teach_title": "How We Teach",
            "teach_cards": [
                {
                    "title": "The Science",
                    "subtitle": "Learn the Core Science Concepts First",
                    "body": "Each project begins by breaking down key robotics and engineering principles, so kids understand the science before they start building.",
                },
                {
                    "title": "The Build",
                    "subtitle": "Turn Concepts into Real Robots",
                    "body": "Once they've learned the science, kids bring it to life with hands-on kits, building real robots that connect ideas to action.",
                },
                {
                    "title": "The Guidance",
                    "subtitle": "Follow Along with Step-by-Step Videos",
                    "body": "Guided video lessons walk kids through each build with clear, practical instruction, making every step easy to follow and fun to complete.",
                },
            ],
            "demo_cta": "See Demo",
            "faq_title": "Frequently Asked Questions",
            "faqs": [
                {
                    "question": "What age group is this program suitable for?",
                    "answer": "Our robotics program is designed for children ages 8-14. We've carefully structured the curriculum to match different learning stages, ensuring each child can progress at their own pace while staying engaged and challenged.",
                },
                {
                    "question": "Do I need any prior experience with robotics?",
                    "answer": "No prior experience is needed! Our program starts with the basics and gradually builds up to more complex concepts. Each kit comes with detailed instructions and video guides that make learning robotics accessible to everyone.",
                },
                {
                    "question": "How long does it take to complete a project?",
                    "answer": "Each project typically takes 2-3 hours to complete, including both building and programming. The modular design allows students to work at their own pace, and they can always revisit projects to try new modifications or improvements.",
                },
                {
                    "question": "What's included in the robotics kit?",
                    "answer": "Each kit includes all necessary components: motors, sensors, microcontroller, building pieces, and detailed instructions. You'll also get access to our online learning platform with video tutorials and programming guides.",
                },
                {
                    "question": "Can I get help if I'm stuck?",
                    "answer": "Absolutely! We provide comprehensive support through our online platform. You can access step-by-step video guides, troubleshooting tips, and even connect with our support team for personalized assistance.",
                },
            ],
            "contact_title": "Contact Us",
            "contact_image_alt": "Contact Us",
            "contact_intro_title": "We'd love to hear from you!",
            "contact_intro_text": "Fill out the form below or reach us on",
            "contact_name": "Your Name",
            "contact_email": "Your Email",
            "contact_reason": "Reason",
            "contact_message": "Your Message",
            "contact_reason_placeholder": "Select a reason",
            "contact_reason_options": [
                {"value": "general", "label": "General Inquiry"},
                {"value": "support", "label": "Support Request"},
                {"value": "feedback", "label": "Feedback/Suggestion"},
                {"value": "partnership", "label": "Partnership Opportunity"},
                {"value": "other", "label": "Other"},
            ],
            "contact_submit": "Send Message",
            "contact_success": "Thank you! Your message has been sent.",
        },
        "buy": {
            "meta_title": "Buy Kit - Brainiacs Academy",
            "image_alt": "Buy Kit",
            "header": "We're Partnering with Schools & Teaching Centers!",
            "body_before_strong": "For now, Brainiacs kits are only available through our educational partners.",
            "body_strong": "Want to be the first to know when kits are available for individuals?",
            "body_after_strong": "Sign up below and we'll notify you as soon as direct shipping opens!",
            "email_placeholder": "Enter your email",
            "notify_me": "Notify Me",
            "enquire": "Enquire",
        },
        "activate": {
            "meta_title": "Activate Kit - Brainiacs Academy",
            "image_alt": "Activate Kit",
            "header": "Activate Your Kit",
            "submit": "Activate & Create Account",
        },
        "confirm_email": {
            "meta_title": "Confirm Email - Brainiacs Academy",
            "heading": "Confirm Your Email",
            "intro_before_email": "Check your inbox for the verification code sent to",
            "intro_after_email": "then enter it below.",
            "resent_success": "A new verification code has been sent.",
            "delivery_warning_prefix": "Verification email was not delivered. Please use",
            "delivery_warning_button": "Resend Code",
            "delivery_warning_suffix": "and check spam/promotions.",
            "confirm_email": "Confirm Email",
            "resend_code": "Resend Code",
            "wrong_email": "Wrong email?",
            "go_back": "Go back",
        },
        "demo": {
            "meta_title": "Demo Page - Brainiacs Academy",
            "hero_title": "Meet Pedro the Dog",
            "hero_intro_main": "Build Pedro, bring him to life with code, and discover the basics of programming, circuits, and movement through hands-on play.",
            "hero_intro_secondary": "Whether you're just starting out or leveling up your STEM skills, Pedro is the perfect companion.",
            "previous": "Previous",
            "next": "Next",
            "pedro_image_alt": "Pedro the Dog",
            "building_image_alt": "Building",
            "demo_video_title": "Pedro Demo Video",
            "tab_science": "The Science",
            "tab_build": "The Build",
            "tab_guidance": "The Guidance",
            "science_intro": "Explore the core science and engineering concepts you'll master with Pedro the Dog.",
            "science_cards": [
                {
                    "title": "Engineering & Robotics",
                    "items": [
                        "Hands-on mechanical assembly",
                        "Robotic movement through motors and servos",
                        "Structural design and component integration",
                    ],
                },
                {
                    "title": "Electronics & Hardware",
                    "items": [
                        "Arduino board basics",
                        "Working with LEDs, resistors, motors, and sensors",
                        "Power flow, breadboard wiring, and circuit logic",
                    ],
                },
                {
                    "title": "Coding & Programming",
                    "items": [
                        "Intro to code structure and logic",
                        "Programming digital and analog inputs/outputs",
                        "Real-time control of lights, motion, and sensors",
                    ],
                },
                {
                    "title": "Core STEM Skills",
                    "items": [
                        "Systems thinking",
                        "Problem-solving and debugging",
                        "Intro to digital vs analog signals",
                        "Building, testing, and iterating like an engineer",
                    ],
                },
            ],
            "build_intro": "See what's inside your kit and how each part helps bring Pedro to life.",
            "build_title": "Kit Components",
            "components": [
                {
                    "name": "Arduino Uno R3 + USB cable",
                    "description": "The programmable brain that powers your robot.",
                },
                {
                    "name": "Breadboard",
                    "description": "A tool to easily prototype and connect electronic components.",
                },
                {
                    "name": "LEDs",
                    "description": "Light-emitting diodes used to signal activity or responses.",
                },
                {
                    "name": "Resistors",
                    "description": "Control the flow of electrical current in circuits.",
                },
                {
                    "name": "Capacitors",
                    "description": "Store and release small bursts of energy when needed.",
                },
                {
                    "name": "Motors",
                    "description": "Enable movement and bring your robot to life.",
                },
                {
                    "name": "IRF520 Transistor",
                    "description": "Acts as a switch to control high-power components.",
                },
                {
                    "name": "1N4007 Diode",
                    "description": "Protects your circuits by blocking reverse current.",
                },
                {
                    "name": "DC Motor",
                    "description": "Drives continuous motion like Pedro's legs.",
                },
                {
                    "name": "Servo Motor",
                    "description": "Provides precise movement for parts like the neck or tail.",
                },
                {
                    "name": "Unique lessons activation code",
                    "description": "Unlocks your interactive Brainiacs learning journey.",
                },
            ],
            "guidance_intro": "Get step-by-step guidance and tips for building, coding, and exploring with Pedro.",
            "video_not_supported": "Your browser does not support the video tag.",
            "buy_pedro": "Buy Pedro",
            "inquire": "Inquire",
        },
        "login": {
            "meta_title": "Sign In | Brainiacs",
            "heading": "Welcome Back",
            "subtitle": "Sign in to access Brainiacs lessons and save progress.",
            "submit": "Sign In",
            "need_account": "Need an account?",
            "create_local_account": "Create a local account",
            "new_here": "New here?",
            "activate_kit_account": "Activate your kit to create an account",
        },
        "signup": {
            "meta_title": "Sign Up | Brainiacs",
            "heading": "Create Account",
            "subtitle_before_link": "Sign up once, then continue into the lessons. You need a valid activation code.",
            "subtitle_link": "Activate your kit first",
            "subtitle_after_link": "",
            "submit": "Create Account",
            "already_have_account": "Already have an account?",
            "sign_in": "Sign in",
        },
        "signup_local": {
            "meta_title": "Create Local Account | Brainiacs",
            "heading": "Create Local Account",
            "subtitle": "Local development mode: activation code is bypassed.",
            "submit": "Create Account",
            "already_have_account": "Already have an account?",
            "sign_in": "Sign in",
        },
    },
    "fr": {
        "common": {
            "brand_display": "ACADÉMIE BRAINIACS",
            "brand_meta": "Académie Brainiacs",
            "buy_kit": "Acheter le kit",
            "contact_us": "Contactez-nous",
            "log_in": "Connexion",
            "activate_kit": "Activer le kit",
            "open_navigation": "Ouvrir la navigation",
            "language_switch": "Choix de la langue",
            "back_to_home": "Retour à l'accueil",
            "footer_copyright": "2025 Académie Brainiacs. Tous droits réservés.",
            "show_password": "Afficher le mot de passe",
            "hide_password": "Masquer le mot de passe",
            "toggle_password": "Afficher ou masquer le mot de passe",
            "username": "Nom d'utilisateur",
            "password": "Mot de passe",
            "confirm_password": "Confirmer le mot de passe",
            "activation_code": "Code d'activation",
            "your_email": "Votre e-mail",
            "verification_code": "Code de vérification",
        },
        "home": {
            "meta_title": "Académie Brainiacs",
            "hero_image_alt": "Kit de construction robotique",
            "hero_title": "La robotique simplifiée",
            "hero_description": "Nos kits robotiques interactifs transforment les esprits curieux en constructeurs confiants.",
            "hero_cta": "Découvrir",
            "mission_title": "Notre mission",
            "mission_lead": "Brainiacs repose sur une conviction :",
            "mission_highlight": "Avec les bons outils, apprendre la robotique devient simple.",
            "mission_text": "Nous rendons l'apprentissage clair, concret et ludique, avec juste le bon niveau de défi.",
            "teach_title": "Comment nous enseignons",
            "teach_cards": [
                {
                    "title": "La science",
                    "subtitle": "Comprendre d'abord les notions scientifiques clés",
                    "body": "Chaque projet commence par une explication claire des principes de robotique et d'ingénierie, afin que les enfants comprennent la science avant de construire.",
                },
                {
                    "title": "La construction",
                    "subtitle": "Transformer les concepts en vrais robots",
                    "body": "Une fois les notions acquises, les enfants leur donnent vie avec des kits pratiques et construisent de vrais robots qui relient les idées à l'action.",
                },
                {
                    "title": "L'accompagnement",
                    "subtitle": "Suivre des vidéos étape par étape",
                    "body": "Des leçons vidéo guidées accompagnent chaque construction avec des explications claires et concrètes, pour rendre chaque étape simple et agréable.",
                },
            ],
            "demo_cta": "Voir la démo",
            "faq_title": "Questions fréquentes",
            "faqs": [
                {
                    "question": "À quel âge ce programme convient-il ?",
                    "answer": "Notre programme de robotique est conçu pour les enfants de 8 à 14 ans. Le parcours a été pensé pour s'adapter aux différentes étapes d'apprentissage, afin que chacun progresse à son rythme tout en restant motivé et stimulé.",
                },
                {
                    "question": "Faut-il déjà avoir une expérience en robotique ?",
                    "answer": "Aucune expérience préalable n'est nécessaire. Notre programme commence par les bases puis avance progressivement vers des notions plus complexes. Chaque kit comprend des instructions détaillées et des vidéos pour rendre la robotique accessible à tous.",
                },
                {
                    "question": "Combien de temps faut-il pour terminer un projet ?",
                    "answer": "Chaque projet prend généralement entre 2 et 3 heures, en comptant la construction et la programmation. La conception modulaire permet aux élèves d'avancer à leur propre rythme et de revenir sur les projets pour tester de nouvelles idées ou améliorations.",
                },
                {
                    "question": "Que contient le kit de robotique ?",
                    "answer": "Chaque kit comprend tous les composants nécessaires : moteurs, capteurs, microcontrôleur, pièces de construction et instructions détaillées. Vous bénéficiez aussi d'un accès à notre plateforme d'apprentissage en ligne avec tutoriels vidéo et guides de programmation.",
                },
                {
                    "question": "Puis-je obtenir de l'aide si je bloque ?",
                    "answer": "Absolument. Nous proposons une assistance complète via notre plateforme en ligne. Vous y trouverez des vidéos pas à pas, des conseils de dépannage et la possibilité de contacter notre équipe pour une aide personnalisée.",
                },
            ],
            "contact_title": "Contactez-nous",
            "contact_image_alt": "Contactez-nous",
            "contact_intro_title": "Nous serions ravis d'échanger avec vous !",
            "contact_intro_text": "Remplissez le formulaire ci-dessous ou contactez-nous sur",
            "contact_name": "Votre nom",
            "contact_email": "Votre e-mail",
            "contact_reason": "Motif",
            "contact_message": "Votre message",
            "contact_reason_placeholder": "Sélectionnez un motif",
            "contact_reason_options": [
                {"value": "general", "label": "Question générale"},
                {"value": "support", "label": "Demande d'assistance"},
                {"value": "feedback", "label": "Retour / suggestion"},
                {"value": "partnership", "label": "Opportunité de partenariat"},
                {"value": "other", "label": "Autre"},
            ],
            "contact_submit": "Envoyer le message",
            "contact_success": "Merci ! Votre message a bien été envoyé.",
        },
        "buy": {
            "meta_title": "Acheter le kit - Académie Brainiacs",
            "image_alt": "Acheter le kit",
            "header": "Nous collaborons avec des écoles et des centres éducatifs !",
            "body_before_strong": "Pour le moment, les kits Brainiacs sont disponibles uniquement via nos partenaires éducatifs.",
            "body_strong": "Vous voulez être informé en premier lorsque les kits seront disponibles pour les particuliers ?",
            "body_after_strong": "Inscrivez-vous ci-dessous et nous vous préviendrons dès que l'expédition directe sera ouverte.",
            "email_placeholder": "Entrez votre e-mail",
            "notify_me": "Prévenez-moi",
            "enquire": "Se renseigner",
        },
        "activate": {
            "meta_title": "Activer le kit - Académie Brainiacs",
            "image_alt": "Activer le kit",
            "header": "Activez votre kit",
            "submit": "Activer et créer un compte",
        },
        "confirm_email": {
            "meta_title": "Confirmer l'e-mail - Académie Brainiacs",
            "heading": "Confirmez votre e-mail",
            "intro_before_email": "Vérifiez votre boîte de réception pour le code de vérification envoyé à",
            "intro_after_email": "puis saisissez-le ci-dessous.",
            "resent_success": "Un nouveau code de vérification a été envoyé.",
            "delivery_warning_prefix": "L'e-mail de vérification n'a pas été distribué. Utilisez",
            "delivery_warning_button": "Renvoyer le code",
            "delivery_warning_suffix": "et vérifiez vos dossiers spam/promotions.",
            "confirm_email": "Confirmer l'e-mail",
            "resend_code": "Renvoyer le code",
            "wrong_email": "Mauvaise adresse e-mail ?",
            "go_back": "Retour",
        },
        "demo": {
            "meta_title": "Démo - Académie Brainiacs",
            "hero_title": "Découvrez Pedro le chien",
            "hero_intro_main": "Construisez Pedro, donnez-lui vie avec du code et découvrez les bases de la programmation, des circuits et du mouvement grâce à un apprentissage pratique.",
            "hero_intro_secondary": "Que vous débutiez ou que vous développiez déjà vos compétences STEM, Pedro est le compagnon idéal.",
            "previous": "Précédent",
            "next": "Suivant",
            "pedro_image_alt": "Pedro le chien",
            "building_image_alt": "Construction",
            "demo_video_title": "Vidéo de démonstration de Pedro",
            "tab_science": "La science",
            "tab_build": "La construction",
            "tab_guidance": "L'accompagnement",
            "science_intro": "Explorez les concepts clés de science et d'ingénierie que vous maîtriserez avec Pedro le chien.",
            "science_cards": [
                {
                    "title": "Ingénierie et robotique",
                    "items": [
                        "Assemblage mécanique pratique",
                        "Mouvement robotique grâce aux moteurs et servomoteurs",
                        "Conception structurelle et intégration des composants",
                    ],
                },
                {
                    "title": "Électronique et matériel",
                    "items": [
                        "Bases de la carte Arduino",
                        "Utilisation des LED, résistances, moteurs et capteurs",
                        "Flux électrique, câblage sur breadboard et logique des circuits",
                    ],
                },
                {
                    "title": "Code et programmation",
                    "items": [
                        "Introduction à la structure et à la logique du code",
                        "Programmation des entrées/sorties numériques et analogiques",
                        "Contrôle en temps réel des lumières, du mouvement et des capteurs",
                    ],
                },
                {
                    "title": "Compétences STEM fondamentales",
                    "items": [
                        "Pensée systémique",
                        "Résolution de problèmes et débogage",
                        "Introduction aux signaux numériques et analogiques",
                        "Construire, tester et itérer comme un ingénieur",
                    ],
                },
            ],
            "build_intro": "Découvrez ce qu'il y a dans votre kit et comment chaque élément aide à donner vie à Pedro.",
            "build_title": "Composants du kit",
            "components": [
                {
                    "name": "Arduino Uno R3 + câble USB",
                    "description": "Le cerveau programmable qui alimente votre robot.",
                },
                {
                    "name": "Breadboard",
                    "description": "Un support qui permet de prototyper et connecter facilement les composants électroniques.",
                },
                {
                    "name": "LED",
                    "description": "Des diodes électroluminescentes utilisées pour signaler une activité ou une réponse.",
                },
                {
                    "name": "Résistances",
                    "description": "Elles contrôlent le flux du courant électrique dans les circuits.",
                },
                {
                    "name": "Condensateurs",
                    "description": "Ils stockent et libèrent de petites impulsions d'énergie lorsque c'est nécessaire.",
                },
                {
                    "name": "Moteurs",
                    "description": "Ils permettent le mouvement et donnent vie à votre robot.",
                },
                {
                    "name": "Transistor IRF520",
                    "description": "Il agit comme un interrupteur pour piloter des composants plus puissants.",
                },
                {
                    "name": "Diode 1N4007",
                    "description": "Elle protège vos circuits en bloquant le courant inverse.",
                },
                {
                    "name": "Moteur DC",
                    "description": "Il produit un mouvement continu, comme les pattes de Pedro.",
                },
                {
                    "name": "Servomoteur",
                    "description": "Il fournit un mouvement précis pour des éléments comme le cou ou la queue.",
                },
                {
                    "name": "Code d'activation des leçons",
                    "description": "Il débloque votre parcours d'apprentissage interactif Brainiacs.",
                },
            ],
            "guidance_intro": "Profitez d'un accompagnement pas à pas et de conseils pour construire, coder et explorer avec Pedro.",
            "video_not_supported": "Votre navigateur ne prend pas en charge la vidéo.",
            "buy_pedro": "Acheter Pedro",
            "inquire": "Se renseigner",
        },
        "login": {
            "meta_title": "Connexion | Brainiacs",
            "heading": "Heureux de vous revoir",
            "subtitle": "Connectez-vous pour accéder aux leçons Brainiacs et enregistrer votre progression.",
            "submit": "Se connecter",
            "need_account": "Besoin d'un compte ?",
            "create_local_account": "Créer un compte local",
            "new_here": "Nouveau ici ?",
            "activate_kit_account": "Activez votre kit pour créer un compte",
        },
        "signup": {
            "meta_title": "Inscription | Brainiacs",
            "heading": "Créer un compte",
            "subtitle_before_link": "Inscrivez-vous une fois, puis poursuivez vers les leçons. Vous avez besoin d'un code d'activation valide.",
            "subtitle_link": "Activez d'abord votre kit",
            "subtitle_after_link": "",
            "submit": "Créer un compte",
            "already_have_account": "Vous avez déjà un compte ?",
            "sign_in": "Se connecter",
        },
        "signup_local": {
            "meta_title": "Créer un compte local | Brainiacs",
            "heading": "Créer un compte local",
            "subtitle": "Mode développement local : le code d'activation est désactivé.",
            "submit": "Créer un compte",
            "already_have_account": "Vous avez déjà un compte ?",
            "sign_in": "Se connecter",
        },
    },
}


FORM_TRANSLATIONS: dict[str, dict[str, dict[str, dict[str, str]]]] = {
    "en": {
        "activate_signup": {
            "username": {"label": "Username", "placeholder": "Username"},
            "activation_code": {"label": "Activation Code", "placeholder": "Activation Code"},
            "email": {"label": "Your Email", "placeholder": "Your Email"},
            "password1": {"label": "Password", "placeholder": "Password"},
            "password2": {"label": "Confirm Password", "placeholder": "Confirm Password"},
        },
        "verify_email": {
            "verification_code": {"label": "Verification code", "placeholder": "6-digit code"}
        },
        "login": {
            "username": {"label": "Username", "placeholder": "Username"},
            "password": {"label": "Password", "placeholder": "Password"},
        },
        "signup_local": {
            "username": {"label": "Username", "placeholder": "Username"},
            "password1": {"label": "Password", "placeholder": "Password"},
            "password2": {"label": "Confirm Password", "placeholder": "Confirm Password"},
        },
    },
    "fr": {
        "activate_signup": {
            "username": {"label": "Nom d'utilisateur", "placeholder": "Nom d'utilisateur"},
            "activation_code": {"label": "Code d'activation", "placeholder": "Code d'activation"},
            "email": {"label": "Votre e-mail", "placeholder": "Votre e-mail"},
            "password1": {"label": "Mot de passe", "placeholder": "Mot de passe"},
            "password2": {"label": "Confirmer le mot de passe", "placeholder": "Confirmer le mot de passe"},
        },
        "verify_email": {
            "verification_code": {"label": "Code de vérification", "placeholder": "Code à 6 chiffres"}
        },
        "login": {
            "username": {"label": "Nom d'utilisateur", "placeholder": "Nom d'utilisateur"},
            "password": {"label": "Mot de passe", "placeholder": "Mot de passe"},
        },
        "signup_local": {
            "username": {"label": "Nom d'utilisateur", "placeholder": "Nom d'utilisateur"},
            "password1": {"label": "Mot de passe", "placeholder": "Mot de passe"},
            "password2": {"label": "Confirmer le mot de passe", "placeholder": "Confirmer le mot de passe"},
        },
    },
}


SITE_MESSAGE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "fr": {
        "Invalid activation code.": "Code d'activation invalide.",
        "This activation code has expired.": "Ce code d'activation a expiré.",
        "This activation code is already linked to an account.": "Ce code d'activation est déjà associé à un compte.",
        "This code was already activated with a different email.": "Ce code a déjà été activé avec une autre adresse e-mail.",
        "This activation code has expired. Try another code.": "Ce code d'activation a expiré. Essayez-en un autre.",
        "This activation code has already been used. Try another code.": "Ce code d'activation a déjà été utilisé. Essayez-en un autre.",
        "This account is not linked to an activation code. Activate your kit before signing in.": "Ce compte n'est associé à aucun code d'activation. Activez votre kit avant de vous connecter.",
        "You must confirm your email before signing in. Check your inbox for the verification code.": "Vous devez confirmer votre e-mail avant de vous connecter. Vérifiez votre boîte de réception pour le code de vérification.",
        "Invalid verification code.": "Code de vérification invalide.",
        "We sent a new verification code to your email.": "Nous avons envoyé un nouveau code de vérification à votre adresse e-mail.",
        "Could not send verification email. Please retry in a moment.": "Impossible d'envoyer l'e-mail de vérification pour le moment. Veuillez réessayer dans un instant.",
        "A new verification code has been sent.": "Un nouveau code de vérification a été envoyé.",
    }
}


def normalize_site_language(lang: str | None) -> str:
    if not lang:
        return DEFAULT_SITE_LANGUAGE
    lang = lang.strip().lower()
    if lang not in SUPPORTED_SITE_LANGUAGES:
        return DEFAULT_SITE_LANGUAGE
    return lang


def get_site_language(request) -> str:
    query_lang = request.GET.get("lang")
    if query_lang in SUPPORTED_SITE_LANGUAGES:
        return normalize_site_language(query_lang)
    return normalize_site_language(request.COOKIES.get(SITE_LANGUAGE_COOKIE))


def get_site_copy(lang: str) -> dict[str, Any]:
    return SITE_COPY[normalize_site_language(lang)]


def translate_site_message(text: str, lang: str) -> str:
    if normalize_site_language(lang) != "fr":
        return text
    return SITE_MESSAGE_TRANSLATIONS["fr"].get(text, text)


def localize_form(form, lang: str, form_key: str):
    translations = FORM_TRANSLATIONS.get(normalize_site_language(lang), {}).get(form_key, {})
    for field_name, field_copy in translations.items():
        field = form.fields.get(field_name)
        if not field:
            continue
        field.label = field_copy["label"]
        field.widget.attrs["placeholder"] = field_copy["placeholder"]
    return form
