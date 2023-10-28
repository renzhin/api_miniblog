echo -e ".separator ", \
        "\n.import static/data/category.csv titles_category" \
        "\n.import static/data/comments.csv titles_comment" \
        "\n.import static/data/genre_title.csv titles_genretitle" \
        "\n.import static/data/genre.csv titles_genre" \
        "\n.import static/data/review.csv titles_review" \
        "\n.import static/data/titles.csv titles_title" \
        "\n.import static/data/users.csv users_myuser" \
        | sqlite3 db.sqlite3
