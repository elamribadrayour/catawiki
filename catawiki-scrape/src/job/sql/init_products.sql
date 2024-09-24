CREATE TABLE IF NOT EXISTS products (
    exec_date TIMESTAMP,
    id_category INTEGER,
    category_name TEXT,
    id BIGINT,
    title TEXT,
    subtitle TEXT,
    thumbImageUrl TEXT,
    originalImageUrl TEXT,
    favoriteCount INTEGER,
    url TEXT,
    localized BOOLEAN,
    translatedTitle TEXT,
    translatedSubtitle TEXT,
    auctionId BIGINT,
    pubnubChannel TEXT,
    useRealtimeMessageFallback BOOLEAN,
    isContentExplicit BOOLEAN,
    reservePriceSet BOOLEAN,
    biddingStartTime TIMESTAMP,
    buyNow TEXT,
    description TEXT,
    sellerId BIGINT,
    sellerShopName TEXT,
    live STRUCT(
        id BIGINT,
        reservePriceMet BOOLEAN,
        bid STRUCT(
            EUR DOUBLE,
            USD DOUBLE,
            GBP DOUBLE
        ),
        biddingEndTime BIGINT,
        biddingStartTime BIGINT,
        highestBidderToken TEXT,
        favoriteCount INTEGER,
        winnerToken TEXT,
        closeStatus TEXT,
        isBuyNowAvailable BOOLEAN
    )
)