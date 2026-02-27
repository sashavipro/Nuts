import './jquery-global.js';
// import '../libs/jquery/dist/jquery.min.js';
import '../libs/select2/dist/js/select2.min.js';

window.addEventListener('load', function() {
    'use strict';

    // Гарантируем, что используем правильный глобальный jQuery
    const $ = window.jQuery;

    // --- 1. Инициализация переменных ---
    const $country = $('#id_country');
    const $region = $('#id_region');
    const $userTypeInput = $('#id_user_type');
    const $isFopCheckbox = $('#id_is_fop');
    const $requisitesBlock = $('#requisitesBlock'); // Блок с названием компании и ОКПО
    const $companyInput = $('#id_company_name');
    const $okpoInput = $('#id_okpo');

    // Получаем URL API из атрибута (или дефолтный)
    const apiUrl = $('#country-wrapper').data('api-url') || "/users/api/regions";

    // --- 2. Select2 и API ---
    if ($.fn.select2) {
        $country.select2({ width: '100%', placeholder: "Выберите страну" });
        $region.select2({ width: '100%', placeholder: "Сначала выберите страну" });
    } else {
        console.error("Select2 не загружен!");
    }

    if (!$country.val()) $region.prop('disabled', true);

    $country.on('change', function() {
        var countryId = $(this).val();
        $region.empty().append('<option value="">Загрузка...</option>').prop('disabled', true);

        if (!countryId) {
            $region.empty().append('<option value="">Сначала выберите страну</option>');
            $region.trigger('change');
            return;
        }

        $.ajax({
            url: apiUrl,
            data: { 'country_id': countryId },
            type: 'GET',
            success: function(data) {
                $region.empty();
                if (data && data.length > 0) {
                    $region.append('<option value="">Выберите регион</option>');
                    $.each(data, function(index, item) {
                        $region.append(new Option(item.name, item.id, false, false));
                    });
                    $region.prop('disabled', false);
                } else {
                    $region.append('<option value="">В этой стране нет регионов</option>');
                }
                $region.trigger('change');
            },
            error: function() {
                $region.empty().append('<option value="">Ошибка загрузки</option>');
                $region.trigger('change');
            }
        });
    });

    // --- 3. ЛОГИКА ТИПОВ ПОЛЬЗОВАТЕЛЯ ---
    function updateFormState() {
        const activeTabType = $('.reg-tab.active').data('type');
        const isFopChecked = $isFopCheckbox.is(':checked');

        if (activeTabType === 'legal') {
            $userTypeInput.val('legal');
            $('#fop-block').hide();
            $requisitesBlock.slideDown();
            $companyInput.prop('required', true);
            $okpoInput.prop('required', true);
        } else {
            $('#fop-block').show();

            if (isFopChecked) {
                $userTypeInput.val('fop');
                $requisitesBlock.slideUp();
                $companyInput.prop('required', false);
                $okpoInput.prop('required', false);
            } else {
                $userTypeInput.val('physical');
                $requisitesBlock.slideUp();
                $companyInput.prop('required', false);
                $okpoInput.prop('required', false);
            }
        }
    }

    // Обработчики событий
    $('.reg-tab').on('click', function(e) {
        e.preventDefault();
        $('.reg-tab').removeClass('active').css({'color': '#aaa', 'border-bottom': '3px solid transparent'});
        $(this).addClass('active').css({'color': '#1d252d', 'border-bottom': '3px solid #337d5a'});
        updateFormState();
    });

    $isFopCheckbox.on('change', function() {
        updateFormState();
    });

    // --- 4. Аватар ---
    $('#id_avatar').on('change', function(e) {
        if(this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#avatar-preview-img').attr('src', e.target.result).show();
                $('#avatar-placeholder').hide();
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    // Запуск при загрузке
    updateFormState();
});
