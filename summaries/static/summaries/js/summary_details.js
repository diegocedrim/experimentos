//Alta granularidade
//
//1 - Padrões de Projeto
//2 - Aglomerações
//3 - Smells
//4 - Princípios de design
//5 - Atributos não funcionais
//
//
//Baixa Granularidade
//1 - Atributos não funcionais
//2 - Princípios de design
//3 - Smells
//4 - Aglomerações
//5 - Padrões de Projeto



var alphabetical = ['agglomerations', 'code_smells', 'non_functional', 'design_patterns', 'design_principles'];

var granularity_desc = ['design_patterns', 'agglomerations', 'code_smells', 'design_principles', 'non_functional'];

var granularity_asc = ['non_functional', 'design_principles', 'code_smells', 'agglomerations', 'design_patterns'];

function sort(order_array){
    var container = $("#basic_information_container")
    for (var i = 0; i < order_array.length; i++) {
        var element_id = "#" + order_array[i];
        var element = $(element_id);
        element.detach();
        container.append(element);
    }
}

function setupRelevanceEvents() {
    var collapsable_panels = ['agg_collapse', 'anomalies_collapse', 'nonfunc_collapse',
        'dpatterns_collapse', 'design_collapse', 'examples_collapse'];
    for (var i = 0; i < collapsable_panels.length; i++) {
        console.log(collapsable_panels[i]);
        $('#' + collapsable_panels[i]).on('show.bs.collapse', function (el) {
            var element_id = "#" + el.target.id;
            $(element_id + " .radio-inline input[type=radio]").prop('required', true);
        });
    }
}

$(document).ready(function(){
    $("form input").on("invalid", function(event) {
        console.log(event.target.name);
        $("input[name=" + event.target.name+ "]").closest(".collapse-caret").find("> .panel-body").collapse('show');
    });
});