<?php
ini_set('display_errors', 1);
require __DIR__ . '/vendor/autoload.php';

if(isset($_GET['source'])) {
    highlight_file('index.php');
    exit();
}

$private_key = file_get_contents('/secrets/private.key');
$public_key = file_get_contents('/secrets/public.key');
$flag = file_get_contents('/secrets/flag.txt');

class JWTUtil {
    function encode($data, $key, $algorithm='HS256') {
        $jwt = new JOSE_JWT($data);
        $jwt = $jwt->sign($key, $algorithm);
        return $jwt->toString();
    }
    
    function decode($token, $key) {
        try {
            $jwt = JOSE_JWT::decode($token);
            $jwt->verify($key, $jwt->header['alg']); // autodetect algorithm
        } catch (Exception $err) {
            return NULL;
        }
        return $jwt->claims;
    }
}

$loader = new \Twig\Loader\FilesystemLoader('templates');
$twig = new \Twig\Environment($loader);

if (!isset($_REQUEST['token'])) {
    $token = JWTUtil::encode(['is_admin' => FALSE], $private_key, 'RS256');
    echo $twig->render('index.html', ['token' => $token, 'error' => 'You need a token']);
} else {
    $token = $_REQUEST['token'];
    $data = JWTUtil::decode($token, $public_key);
    if($data && $data['is_admin'] === TRUE) {
        echo $twig->render('index.html', ['token' => $token, 'flag' => $flag]);
    } else {
        echo $twig->render('index.html', ['token' => $token, 'error' => 'You are not admin.']);
    }
}
?>