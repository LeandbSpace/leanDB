<?php
    require_once('func.php');
    $allposts = dryQuery( '{"action": "FETCH_DATA","databaseName": "goldposts","tableName": "posts","columns": "*","limit": {"count": "10","skip": "0"},"where": {"_strict": { "user": "hasan" },"eq": { "userid": "2102", "post_status": "1" },"gt": { "votes": "10" },"lt": { "downvotes": "5" },"bt": {"votes": "5,10" }}}' );
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

            foreach( $allposts->items as $post ) {
                echo '<div style="font-size: 20px;"><a href="/singlepost.php?slug='.$post->slug.'">'.$post->title.'</a></div>';
                echo '<div style="padding: 10px; background-color:#494949;margin:10px;border-radius:10px;">'.$post->content.'</div>';
            }

        ?>

    </div>

</body>
</html>