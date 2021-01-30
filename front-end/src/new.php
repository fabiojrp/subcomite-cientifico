<?php

// Estrutura basica do grafico
$grafico = array(
    'dados' => array(
        'cols' => array(
            array('type' => 'string', 'label' => 'Meses'),
            array('type' => 'number', 'label' => 'Casos'),
            array('type' => 'number', 'label' => 'Obitos')
        ),  
        'rows' => array()
    ),
    'config' => array(
        'title' => 'Quantidade de Casos e Obitos',
        'width' => 1000,
        'height' => 300
    )
);

// Consultar dados no BD
try{
    // $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=;user=covid;password=WEpJqsYMnHWB');
   $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=dump;user=postgres;password=zzdz0737');

}catch(PDOException $e){
     echo $e-> getMessage();
}

#$sql = "SELECT casos.casos, casos.obitos, casos.populacao FROM casos";
    
# Dentro da instrução SQL, tem o comando abaixo que define a regional.
#    regionais.id = 4
    $sql = <<<'SQL'
            SELECT
               casos.data as data,
               sum(casos.casos) as casos_dia,
               sum(casos.obitos) as obitos_dias,
               sum(casos.casos_acumulados) as casos_acumulados,
               sum(casos.obitos_acumulados) as obitos_acumulados,
               to_char(sum(casos.casos_mediaMovel), '99990d999999') as casos_mediaMovel,
               to_char(sum(casos.obitos_mediaMovel), '99990d999999') as obitos_mediaMovel,
               to_char(avg(casos.casos_acumulados_100mil), '99990d999999') as casos_acumulados_100mil,
               to_char(avg(casos.obitos_acumulados_100mil), '99990d999999') as obitos_acumulados_100mil
           FROM regionais, casos
           where casos.regional = regionais.id AND  regionais.id = 4 group by regionais.regional_saude, casos.data ORDER BY casos.data
    SQL;


$statement = $pdo->query($sql);



$dados = array();
    
    //COLUNAS
$dados['cols'] = array(
           array('label' => 'Data', 'type' => 'date'),
           array('label' => 'Casos', 'type' => 'number')
    );
 
    // Dados
$linhas = array();
foreach($statement as $obj) {
    //print_r($obj);
    $data = explode('-', $obj["data"]); // Para formatar o data na próxima etapa
    $temp = array();
    $temp[] = array('v' => (string) "Date($data[0], $data[1], $data[2])"); // Precisa enviar desse formato para o google.visualization.DataTable entender
    $temp[] = array('v' => (int) $obj["casos_dia"]);// Estou utilizando apenas o segundo indicador da consulta SQL

    $linhas[] = array('c' => $temp);
}

$dados['rows'] = $linhas;
    
// Enviar dados na forma de JSON
header('Content-Type: application/json; charset=UTF-8');
echo json_encode($dados);
exit(0);
