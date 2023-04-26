#HACEMOS LAS INSTRUCCIONES CUANDO NOSOTROS GENEREMOS NUESTRA BASE DE DATOS 
instructions = [
    'DROP TABLE IF EXISTS email',
    """
        CREATE TABLE email (
            id INT PRIMARY KEY AUTO_INCREMENT,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """
]
