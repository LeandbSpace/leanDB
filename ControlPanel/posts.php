<?php
    require_once('func.php');
    $allposts = dryQuery( '{"action": "FETCH_DATA", "databaseName": "goldposts", "tableName": "posts", "columns": [ "title", "slug", "category" ], "limit": { "count": "10", "skip": "0" }, "where": { "eq" : [{ "category": "Local News" }, { "category": "Health" }, { "category": "World News" }] }, "sort": { "votes": "desc", "comments_count": "desc" } }' );
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>leanDB Control Panel</title>
    <link rel="stylesheet" href="/assets/leandb_cp.css">
</head>
<body>
    <div class="container">
        <h1>Posts</h1>
        <?php
            // print_r( $allposts );

            foreach( $allposts->data as $post ) {
                echo '<div style="font-size: 20px;"><a href="/singlepost.php?slug='.$post->slug.'">'.$post->title.'</a></div>';
            }

        ?>

    </div>

</body>
</html>