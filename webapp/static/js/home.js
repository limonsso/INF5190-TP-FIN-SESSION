var etablissements = [];
var quickSeacrhResult = [];
$("#quick-search-submit").click(function (e) {
    e.preventDefault();
    var date_du = $("#date_du");
    var date_au = $("#date_au");
    var etablissement_autocomplete = $("#etablissement_autocomplete");
    var contrevenant_id = $("#qck-srch-contrevenant-id");
    if (date_du.val() === "") {
        date_du.addClass("is-invalid");
        return;
    } else {
        if (date_du.hasClass("is-invalid")) date_du.removeClass("is-invalid");
    }
    if (date_au.val() === "") {
        date_au.addClass("is-invalid");
        return;
    } else {
        if (date_au.hasClass("is-invalid")) date_au.removeClass("is-invalid");
    }

    if (
        contrevenant_id.val() === "" ||
        !etablissements.find((x) => x.value === contrevenant_id.val().trim())
    ) {
        etablissement_autocomplete.addClass("is-invalid");
        return;
    } else {
        if (etablissement_autocomplete.hasClass("is-invalid"))
            etablissement_autocomplete.removeClass("is-invalid");
    }

    var alert_qck_search = $("#alert-error-qck-search");
    if (date_du.val() > date_au.val()) {
        alert_qck_search.removeClass("hidden");
    } else {
        if (!alert_qck_search.hasClass("hidden")) {
            alert_qck_search.addClass("hidden");
            return;
        }
    }

    fetch(
        `${
            window.location.origin
        }/contrevenants/contraventions?du=${date_du.val()}&au=${date_au.val()}&contrevenant-id=${contrevenant_id.val()}`
    )
        .then(function (data) {
            data.json().then(function (response) {
                quickSeacrhResult = response;
                fill_qck_search_table(quickSeacrhResult);
            });
        })
        .catch(function (error) {
            console.log(error);
        });
});

function fill_qck_search_table(quickSeacrhResult) {
    $("#quick-search-result tbody").empty();
    var html = "";
    quickSeacrhResult.forEach((elt, index) => {
        html += `<tr>
                    <td scope="row">${elt.date_infraction}</td>
                    <td scope="row" class="parentCell">${elt.description.slice(
            0,
            100
        )}...
                        <span class="tooltip1">${elt.description}</span>
                    </td>
                    <td scope="row">${elt.date_jugement}</td>
                    <td scope="row">${elt.montant}</td>
                 </tr>`;
    });
    if(html===''){
        html=`<tr>
                <td colspan="4" style="text-align: center">Aucun resultat pour cette recherche</td>
            </tr>`
    }
    $("#quick-search-result tbody:last-child").append(html);

    getPagination("#quick-search-result");
}



$(document).ready(function () {
    fill_etablissements_select()
});



function fill_etablissements_select() {
    fetch(`${window.location.origin}/contrevenants`)
        .then((response) => {
            if (response.ok) {
                response.json().then((data) => {
                    etablissements = data.map(x => {
                        return {value: x.id, text: `${x.etablissement} - ${x.proprietaire}`}
                    });
                    autocomplete(
                        document.getElementById("etablissement_autocomplete"),
                        document.getElementById("qck-srch-contrevenant-id"),
                        etablissements
                    );
                });
            }
        })
        .catch((error) => {
            console.log(`Request failed: ${error}`);
        });
}
