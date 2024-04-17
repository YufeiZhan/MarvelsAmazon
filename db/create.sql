CREATE TABLE Users (
    uid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(30) NOT NULL,
    lastname VARCHAR(30) NOT NULL,
    balance DECIMAL(12,2) NOT NULL DEFAULT 0 CHECK (balance >=0),
    role_indicator INT NOT NULL
);

CREATE TABLE Products (
    pid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(255) NOT NULL,
    type VARCHAR(30) NOT NULL,
    creator_id INT REFERENCES Users(uid)
);

CREATE TABLE Inventory (
    iid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    pid INT NOT NULL REFERENCES Products(pid),
    seller_id INT NOT NULL REFERENCES Users(uid),
    unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price > 0),
    quantity_available INT NOT NULL DEFAULT 0 CHECK (quantity_available >=0)
);

CREATE TABLE CartItems (
    uid INT NOT NULL REFERENCES Users(uid),
    iid INT NOT NULL REFERENCES Inventory(iid),
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >=0),
    status INT NOT NULL DEFAULT 1
);

CREATE TABLE Orders (
    oid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(uid),
    address VARCHAR(255) NOT NULL,
    time_placed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    discount FLOAT NOT NULL DEFAULT 1 CHECK (discount > 0 AND discount <= 1)
);

CREATE TABLE OrderItems (
    oiid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    oid INT NOT NULL REFERENCES Orders(oid),
    iid INT NOT NULL REFERENCES Inventory(iid),
    quantity_purchased INT NOT NULL CHECK (quantity_purchased >=0),
    item_status VARCHAR(30) NOT NULL DEFAULT 'placed'
);

CREATE TABLE Coupon (
    code VARCHAR NOT NULL PRIMARY KEY,
    discount FLOAT NOT NULL
);

CREATE TABLE SellerReview (
    seller_id INT NOT NULL REFERENCES Users(uid),
    buyer_id INT NOT NULL REFERENCES Users(uid),
    content VARCHAR(255),
    rating FLOAT NOT NULL DEFAULT 0 CHECK (rating >=0),
    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    upvotes INT NOT NULL DEFAULT 0 CHECK (upvotes >=0),
    PRIMARY KEY (seller_id, buyer_id)
);

CREATE TABLE ProductReview (
    buyer_id INT NOT NULL REFERENCES Users(uid),
    iid INT NOT NULL REFERENCES Inventory(iid),
    content VARCHAR(255),
    rating FLOAT NOT NULL DEFAULT 0 CHECK (rating >=0),
    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    upvotes INT NOT NULL DEFAULT 0 CHECK (upvotes >=0),
    PRIMARY KEY (buyer_id, iid)
);