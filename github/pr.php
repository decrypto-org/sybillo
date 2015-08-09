<?php
  function generateRandomString( $length = 10 ) {
      $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
      $charactersLength = strlen( $characters );
      $randomString = '';
      for ( $i = 0; $i < $length; $i++ ) {
          $randomString .= $characters[rand( 0, $charactersLength - 1 )];
      }
      return $randomString;
  }
  for ( $i = 0; $i < 8; ++$i ) {
    $myfile = fopen( generateRandomString( 5 ) . '.php', "w" );
    fwrite( $myfile, generateRandomString(  200  )  );
    fclose( $myfile  );
    $branch = generateRandomString( 10 );
    shell_exec( "git checkout -b " . $branch );
    shell_exec( "git commit -am '" . generateRandomString( 10 ) . "'" );
    shell_exec( "git push origin " . $branch );
    shell_exec( "hub pull-request -f -m 'Implemented update' -h sybiliansybiler842064670:" . $branch . " -b spasmilo:master" );
  }
?>
