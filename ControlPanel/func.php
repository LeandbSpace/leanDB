<?php

    function httpPost($url, $data) {
        $curl = curl_init($url);
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($curl);
        curl_close($curl);
        return $response;
    }

    // function leanDBString($str) {
    //     $str = str_replace( '"', '\"', $str );
    //     $str = str_replace( "\n\r", "\\n\\r", $str );
    //     $str = str_replace( "\n", "\\n", $str );
    //     $str = str_replace( '\\', '\\\\', $str );
    //     $str = preg_replace('/\s+/', '', $str);
    //     return $str;
    // }

    function sendData( $dataArray = [] ){

        if(empty($dataArray)) return false;

        // $content = str_replace("\n")

        $insertableData = [
            'title' => $dataArray['title'],
            'snippet' => $dataArray['snippet'],
            'content' => $dataArray['content'],
            'category' => $dataArray['category']
        ];

        $q = '{ "action": "INSERT_DATA", "databaseName": "goldposts", "tableName": "posts", "data": '.json_encode($insertableData).', "_index": "title, snippet, category" }';

        $url = "http://127.10.5.10:5925/query";


        $response = httpPost($url, [ 'cmd' => $q ] );

        return json_decode($response);

        // echo '<pre>';
        // print_r($q);
        // echo '</pre>';

        // $q = '{ "action": "INSERT_DATA", "databaseName": "goldposts", "tableName": "posts", "data": {
        //             "title": "'.addslashes($dataArray['title']).'",
        //             "snippet": "'.addslashes($dataArray['snippet']).'",
        //             "content": "'.addslashes($dataArray['content']).'",
        //             "category": "'.addslashes($dataArray['category']).'"
        //         },
        //         "_index": "title, snippet, category"
        //     }
        // ';

        // $url = "http://127.10.5.10:5925/query";

        // echo '<pre>';
        // print_r( $q );
        // echo '</pre>';

        // echo httpPost( 'http://127.0.0.1:5555/index.php', [ 'cmd' => $q ] );

    }