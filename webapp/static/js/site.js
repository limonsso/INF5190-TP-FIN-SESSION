var etablissements = [];
var quickSeacrhResult = [];
$("#quick-search-submit").click(function (e) {
  e.preventDefault();
  var date_du = $("#date_du");
  var date_au = $("#date_au");
  var etablissement_autocomplete = $("#etablissement_autocomplete");
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
    etablissement_autocomplete.val() === "" ||
    !etablissements.find((x) => x === etablissement_autocomplete.val().trim())
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
    }/contrevenants?du=${date_du.val()}&au=${date_au.val()}&etablissement=${etablissement_autocomplete.val()}`
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
                    <td scope="row">${elt.proprietaire}</td>
                    <td scope="row">${elt.categorie}</td>
                    <td scope="row">${elt.etablissement}</td>
                    <td scope="row">${elt.adresse}</td>
                    <td scope="row">${elt.ville}</td>
                    <td scope="row" class="parentCell">${elt.description.slice(
                      0,
                      100
                    )}...
                        <span class="tooltip1">${elt.description}</span>
                    </td>
                    <td scope="row">${elt.date_jugement}</td>
                    <td scope="row">${elt.date_infraction}</td>
                    <td scope="row">${elt.montant}</td>
                    <td scope="row">
                        <a class="btn btn-info" data-toggle="modal" data-target="#edit_contrevenant"
                           data-id="${elt.id}" data-proprietaire="${
      elt.proprietaire
    }"
                           data-etablissement="${elt.etablissement}"
                           data-description="${elt.description}"
                           data-date_jugement="${elt.date_jugement}"
                           data-date_infraction="${elt.date_infraction}"
                           data-montant="${elt.montant}" data-from="qck-search">
                        <span class="fa fa-pencil-square-o text-light"></span></a>
                        <a class="btn btn-danger" onclick="delete_contrevenant('${
                          elt.id
                        }')">
                        <span class="fa fa-trash-o text-light"></span></a>
                    </td>
                 </tr>`;
  });
  $("#quick-search-result tbody:last-child").append(html);

  getPagination("#quick-search-result");
}

$("#edit_contrevenant").on("show.bs.modal", function (e) {
  var contrevenant = e.relatedTarget.dataset;
  console.log(contrevenant);
  $("#contrevenant-id").val(contrevenant.id);
  $("#contrevenant-proprietaire").val(contrevenant.proprietaire);
  $("#contrevenant-etablissement").append(contrevenant.etablissement);
  $("#contrevenant-description").val(contrevenant.description);
  $("#contrevenant-date-jugement").val(contrevenant.date_jugement);
  $("#contrevenant-date-infraction").val(contrevenant.date_infraction);
  $("#contrevenant-montant").val(contrevenant.montant.split(" ")[0]);
  $("#edit-from").val(contrevenant.from);
});

$("#btnUpdateContrevenant").click(function (e) {
  $(".contrevenantEditionForm").submit();
});

$(document).ready(function () {
  $(".contrevenantEditionForm")
    .bootstrapValidator({
      fields: {
        contrevenant_description: {
          validators: {
            notEmpty: {
              message:
                "La description de contrevenant est réquis et ne peut être vide",
            },
          },
        },
        contrevenant_date_jugement: {
          validators: {
            date: {
              format: "MM/DD/YYYY",
              message: "L'entrée n'est pas valide",
            },
            callback: {
              message:
                "La date de jugement doit être superieure à la date d'infraction",
              callback: function (value, validator, $field) {
                return $("#contrevenant-date-infraction").val() < value;
              },
            },
          },
        },
        contrevenant_montant: {
          validators: {
            greaterThan: {
              inclusive: false,
              value: 0,
              message: "Le montant doit être superieur a zéro",
            },
          },
        },
      },
    })
    .on("success.form.bv", function (e) {
      // Prevent form submission
      e.preventDefault();

      var data = {
        id: $("#contrevenant-id").val(),
        description: $("#contrevenant-description").val(),
        date_jugement: $("#contrevenant-date-jugement").val(),
        montant: parseInt($("#contrevenant-montant").val()),
      };
      update_contrevenant(data, $("#edit-from").val());
    });
});

function delete_contrevenant(id) {
  Swal.fire({
    title: "Suppression de contrevenant!",
    text: "Voulez-vous vraiment supprimer ce contrevenant ?",
    icon: "warning",
    showCancelButton: true,
    cancelButtonText: "Non",
    confirmButtonText: "Oui",
    preConfirm: function () {
      return fetch(`${window.location.origin}/contrevenants/${id}`, {
        method: "DELETE",
      })
        .then((response) => {
          console.log(response);
          if (!response.ok) {
            throw new Error(response.statusText);
          }
          Swal.fire({
            title: "Suppression de contravention!",
            text: "La contravention a été supprimée avec succès",
            icon: "success",
            preConfirm: function () {
              location.reload();
            },
          });
        })
        .catch((error) => {
          Swal.showValidationMessage(`Request failed: ${error}`);
        });
    },
  });
}

function update_contrevenant(data, from) {
  console.log(data);
  fetch(`${window.location.origin}/contrevenants/${data.id}`, {
    method: "PUT",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      //return response.json();
      var Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
        onOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
        onClose: () => {
          if (from !== "qck-search") {
            location.reload();
          } else {
            quickSeacrhResult.forEach((elt) => {
              if (elt.id == data.id) {
                (elt.description = data.description),
                (elt.date_jugement = data.date_jugement),
                (elt.montant = `${data.montant} $`);
              }
            });
            fill_qck_search_table(quickSeacrhResult);
            $("#edit_contrevenant").modal("hide");
          }
        },
      });
      if (!response.ok) {
        Toast.fire({
          icon: "error",
          title: "Signed in successfully",
        });
      } else
        Toast.fire({
          icon: "success",
          title: "Signed in successfully",
        });
    })
    .catch((data) => {
      console.log(data);
    });
}

function fill_etablissements_select() {
  fetch(`${window.location.origin}/contrevenants/etablissements`)
    .then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          etablissements = data;
          autocomplete(
            document.getElementById("etablissement_autocomplete"),
            data
          );
        });
      }
    })
    .catch((error) => {
      console.log(`Request failed: ${error}`);
    });
}
