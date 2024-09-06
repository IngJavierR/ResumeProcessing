-- Creación de tablas principales
CREATE TABLE Consultores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(100),
    direccion VARCHAR(255),
    fecha_ingreso DATE,
    descripcion TEXT
);

CREATE TABLE Experiencia_Laboral (
    id SERIAL PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    empresa VARCHAR(100) NOT NULL,
    puesto VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE,
    descripcion TEXT
);

CREATE TABLE Actividades (
    id SERIAL PRIMARY KEY,
    experiencia_id INT REFERENCES Experiencia_Laboral(id),
    descripcion TEXT
);

CREATE TABLE Conocimientos_Tecnicos (
    id SERIAL PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    conocimiento VARCHAR(100) NOT NULL,
    nivel VARCHAR(50)
);

CREATE TABLE Idiomas (
    id SERIAL PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    idioma VARCHAR(50) NOT NULL,
    nivel VARCHAR(50)
);

CREATE TABLE Certificaciones (
    id SERIAL PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    certificacion VARCHAR(100) NOT NULL,
    institucion VARCHAR(100),
    fecha_obtencion DATE,
    fecha_expiracion DATE
);

CREATE TABLE Herramientas (
    id SERIAL PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    herramienta VARCHAR(100) NOT NULL,
    nivel VARCHAR(50)
);

CREATE TABLE Educacion (
    id SERIAL PRIMARY KEY,
    consultor_id INT REFERENCES Consultores(id),
    institucion VARCHAR(100) NOT NULL,
    titulo VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE
);

-- Creación de tablas auxiliares (catálogos)
CREATE TABLE Niveles_Conocimiento (
    id SERIAL PRIMARY KEY,
    nivel VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Niveles_Idiomas (
    id SERIAL PRIMARY KEY,
    nivel VARCHAR(50) UNIQUE NOT NULL
);
