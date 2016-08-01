<?php
    require_once('func.php');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>leanDB Control Panel</title>
    <link rel="stylesheet" href="/assets/leandb_cp.css">
</head>
<body>
    <div class="container tc">
        <h1>Add New News</h1>
        <form action="index.php" method="POST">
            <input type="text" name="title" placeholder="news title here"> <br>
            <textarea name="snippet" rows="5" placeholder="news snippet here"></textarea> <br>
            <textarea name="content" rows="10" placeholder="news content here"></textarea> <br>
            <select name="category">
                <option>World News</option>
                <option>Local News</option>
                <option>Politics</option>
                <option>Sports</option>
                <option selected>Technology</option>
            </select> <br><br>
            <input type="submit" value="Publish News">
        </form>
    </div>

    <?php
        if( isset($_POST['title']) ) {
            echo '<div class="container tc">';
            echo '<pre>';
            print_r($_POST);
            echo '</pre>';
            echo '</div>';

            echo '<div class="container tc">';
            sendData( $_POST );
            echo '</div>';
        }
    ?>

</body>
</html>