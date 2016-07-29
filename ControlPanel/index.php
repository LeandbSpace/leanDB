<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>leanDB Control Panel</title>
    <link rel="stylesheet" href="leandb_cp.css">
</head>
<body>
    <h1>Add New News</h1>
    <form action="index.php" method="POST">
        <input type="text" name="title" placeholder="news title here"> <br>
        <textarea name="snippet" cols="30" rows="10" placeholder="news snippet here"></textarea> <br>
        <textarea name="content" cols="30" rows="10" placeholder="news content here"></textarea> <br>
        <select name="category" id="">
            <option>World News</option>
            <option>Local News</option>
            <option>Politics</option>
            <option>Sports</option>
            <option>Technology</option>
        </select> <br>
        <input type="submit" value="Publish News">
    </form>
</body>
</html>