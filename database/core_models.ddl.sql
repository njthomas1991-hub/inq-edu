PRAGMA foreign_keys = ON;

-- DDL generated from backend/core/models.py (SQLite dialect)

CREATE TABLE core_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),

    -- Custom fields from User(AbstractUser)
    role VARCHAR(20) NOT NULL,
    school VARCHAR(255),
    bio TEXT,
    plain_password VARCHAR(100),
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE core_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    teacher_id INTEGER NOT NULL,
    subject VARCHAR(100) NOT NULL,
    year_ks VARCHAR(2) NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (teacher_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_classstudent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    clazz_id INTEGER NOT NULL,
    date_joined DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (student_id) REFERENCES core_user(id) ON DELETE CASCADE,
    FOREIGN KEY (clazz_id) REFERENCES core_class(id) ON DELETE CASCADE,
    UNIQUE (student_id, clazz_id)
);

CREATE TABLE core_schoolanalyticsprofile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL UNIQUE,
    school VARCHAR(255) NOT NULL,
    can_access_all_teachers BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (teacher_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_newsannouncement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    author_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    status VARCHAR(10) NOT NULL DEFAULT 'draft',
    featured BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    published_at DATETIME,
    FOREIGN KEY (author_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_helptutorial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    author_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    image VARCHAR(255),
    status VARCHAR(10) NOT NULL DEFAULT 'draft',
    featured BOOLEAN NOT NULL DEFAULT 0,
    "order" INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    published_at DATETIME,
    FOREIGN KEY (author_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_teachingresource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    author_id INTEGER NOT NULL,
    content TEXT,
    excerpt TEXT,
    image VARCHAR(255),
    file VARCHAR(255),
    notes TEXT,
    description TEXT,
    resource_type VARCHAR(20) NOT NULL DEFAULT 'other',
    key_stage VARCHAR(10),
    document VARCHAR(255),
    subject VARCHAR(100),
    status VARCHAR(10) NOT NULL DEFAULT 'draft',
    featured BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    published_at DATETIME,
    FOREIGN KEY (author_id) REFERENCES core_user(id) ON DELETE CASCADE
);

-- Many-to-many table for TeachingResource.likes (TeachingResource <-> User)
CREATE TABLE core_teachingresource_likes (
    teachingresource_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (teachingresource_id, user_id),
    FOREIGN KEY (teachingresource_id) REFERENCES core_teachingresource(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_forumpost (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    image VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    is_pinned BOOLEAN NOT NULL DEFAULT 0,
    is_locked BOOLEAN NOT NULL DEFAULT 0,
    views INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (author_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_forumreply (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (post_id) REFERENCES core_forumpost(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_resourcecomment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (resource_id) REFERENCES core_teachingresource(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_avatar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    body_type VARCHAR(20) NOT NULL DEFAULT 'blob',
    body_color VARCHAR(7) NOT NULL DEFAULT '#FF6B9D',
    eye_type VARCHAR(20) NOT NULL DEFAULT 'big_round',
    mouth_type VARCHAR(20) NOT NULL DEFAULT 'happy',
    head_decoration VARCHAR(20) NOT NULL DEFAULT 'horns',
    decoration_color VARCHAR(7) NOT NULL DEFAULT '#FFB347',
    pattern VARCHAR(20) NOT NULL DEFAULT 'solid',
    pattern_color VARCHAR(7) NOT NULL DEFAULT '#FF1493',
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE
);

CREATE TABLE core_kindlewickgameprogress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_type VARCHAR(50) NOT NULL,
    current_level INTEGER NOT NULL DEFAULT 1,
    score INTEGER NOT NULL DEFAULT 0,
    tokens_earned INTEGER NOT NULL DEFAULT 0,
    total_playtime INTEGER NOT NULL DEFAULT 0,
    last_played DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE,
    UNIQUE (user_id, game_type)
);

CREATE TABLE core_kindlewickgamesession (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_type VARCHAR(50) NOT NULL,
    level INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    tokens_earned INTEGER NOT NULL DEFAULT 0,
    playtime INTEGER NOT NULL DEFAULT 0,
    completed BOOLEAN NOT NULL DEFAULT 0,
    session_data JSON DEFAULT (json('{}')),
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    finished_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE
);
