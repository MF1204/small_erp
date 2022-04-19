(function ($$1) {
    'use strict';

    $$1 = 'default' in $$1 ? $$1['default'] : $$1;

    // FilterMenu 변수 선언
    var FilterMenu = function () {
        function FilterMenu(target, th, column, index, options) {
            this.options = options;
            this.th = th;
            this.column = column;
            this.index = index;
            this.tds = target.find('tbody tr td:nth-child(' + (this.column + 1) + ')').toArray();
        }

        // FilterMenu 초기값 설정
        FilterMenu.prototype.initialize = function () {
            this.menu = this.dropdownFilterDropdown();
            // th 에 정렬기능 붙이기
            this.th.appendChild(this.menu);
            // trigger 변수 선언
            var $trigger = $(this.menu.children[0]);
            // content 변수 선언
            var $content = $(this.menu.children[1]);
            // menu 변수 선언
            var $menu = $(this.menu);
            // trigger 를 클릭하면 content 가 토글된다
            $trigger.click(function () {
                // console.log('trigger is working!')
                return $content.toggle();
            });

            $(document).click(function (el) {
                if (!$menu.is(el.target) && $menu.has(el.target).length === 0) {
                    $content.hide();
                    // console.log('------ here is >>> initialize ---------------')
                }
            });
        };

        // FilterMenu 검색 toggle
        // console.log('------ here is >>> searchToggle ---------------')
        FilterMenu.prototype.searchToggle = function (value) {
            // 만약 selectAllCheckbox 의 prototype 속성이 HTMLInputElement 의 instance 에 속한다면
            // 선택된(checked) selectAllCheckbox = false
            if (this.selectAllCheckbox instanceof HTMLInputElement) this.selectAllCheckbox.checked = false;
            console.log(this);
            if (value.length === 0) {
                console.log(value.length)
                this.toggleAll(true);
                if (this.selectAllCheckbox instanceof HTMLInputElement) this.selectAllCheckbox.checked = true;
                return;
            }
            this.toggleAll(false);
            this.inputs.filter(function (input) {
                return input.value.toLowerCase().indexOf(value.toLowerCase()) > -1;
            }).forEach(function (input) {
                input.checked = true;
            });
        };
        // console.log('------ here is >>> searchToggle ---------------')

        // 선택된 것들 update
        FilterMenu.prototype.updateSelectAll = function () {
            if (this.selectAllCheckbox instanceof HTMLInputElement) {
                $(this.searchFilter).val('');
                this.selectAllCheckbox.checked = this.inputs.length === this.inputs.filter(function (input) {
                    return input.checked;
                }).length;
            }
        };

        // 모두 선택
        FilterMenu.prototype.selectAllUpdate = function (checked) {
            $(this.searchFilter).val('');
            this.toggleAll(checked);
        };

        // 모두 토글
        FilterMenu.prototype.toggleAll = function (checked) {
            for (var i = 0; i < this.inputs.length; i++) {
                var input = this.inputs[i];
                if (input instanceof HTMLInputElement) input.checked = checked;
            }
        };

        // 선택목록 DropdownFilterItem
        FilterMenu.prototype.dropdownFilterItem = function (td, self) {
            var value = td.innerText;
            var dropdownFilterItem = document.createElement('div');
            dropdownFilterItem.className = 'dropdown-filter-item';
            var input = document.createElement('input');
            input.type = 'checkbox';
            input.value = value.trim().replace(/ +(?= )/g, '');
            input.setAttribute('checked', 'checked');
            input.className = 'dropdown-filter-menu-item item';
            input.setAttribute('data-column', self.column.toString());
            input.setAttribute('data-index', self.index.toString());
            dropdownFilterItem.appendChild(input);
            dropdownFilterItem.innerHTML = dropdownFilterItem.innerHTML.trim() + ' ' + value;
            return dropdownFilterItem;
        };

        // 선택목록 DropdownFilterItem - 모두 선택
        FilterMenu.prototype.dropdownFilterItemSelectAll = function () {
            var value = this.options.captions.select_all;
            var dropdownFilterItemSelectAll = document.createElement('div');
            dropdownFilterItemSelectAll.className = 'dropdown-filter-item';
            var input = document.createElement('input');
            input.type = 'checkbox';
            input.value = this.options.captions.select_all;
            input.setAttribute('checked', 'checked');
            input.className = 'dropdown-filter-menu-item select-all';
            input.setAttribute('data-column', this.column.toString());
            input.setAttribute('data-index', this.index.toString());
            dropdownFilterItemSelectAll.appendChild(input);
            dropdownFilterItemSelectAll.innerHTML = dropdownFilterItemSelectAll.innerHTML + ' ' + value;
            return dropdownFilterItemSelectAll;
        };

        // 직접 입력하여 검색 DropdownFilterSearch
        FilterMenu.prototype.dropdownFilterSearch = function () {
            var dropdownFilterItem = document.createElement('div');
            dropdownFilterItem.className = 'dropdown-filter-search';

            // var div = document.createElement('span');
            //
            // var input = document.createElement('input');
            // input.type = 'text';
            // input.className = 'dropdown-filter-menu-search form-control';
            // input.setAttribute('data-column', this.column.toString());
            // input.setAttribute('data-index', this.index.toString());
            // //input.setAttribute('placeholder', this.options.captions.search);
            // input.setAttribute('id', "search_input");
            // input.setAttribute('style', "padding: 0;");
            // //input.setAttribute('onkeyup', "return true;");
            // //div.appendChild(input);
            // dropdownFilterItem.appendChild(input);
            // console.log('dropdownFilterItem === ' + dropdownFilterItem);
            return dropdownFilterItem;
        };

        // 선택목록 정렬
        FilterMenu.prototype.dropdownFilterSort = function (direction) {
            var dropdownFilterItem = document.createElement('div');
            dropdownFilterItem.className = 'dropdown-filter-sort';
            var span = document.createElement('span');
            span.className = direction.toLowerCase().split(' ').join('-');
            span.setAttribute('data-column', this.column.toString());
            span.setAttribute('data-index', this.index.toString());
            span.innerText = direction;
            dropdownFilterItem.appendChild(span);
            return dropdownFilterItem;
        };

        // 선택목록 내용
        FilterMenu.prototype.dropdownFilterContent = function () {
            var _this = this;
            var self = this;
            var dropdownFilterContent = document.createElement('div');
            dropdownFilterContent.className = 'dropdown-filter-content';
            var innerDivs = this.tds.reduce(function (arr, el) {
                var values = arr.map(function (el) {
                    return el.innerText.trim();
                });
                if (values.indexOf(el.innerText.trim()) < 0) arr.push(el);
                return arr;
            }, []).sort(function (a, b) {
                var A = a.innerText.toLowerCase();
                var B = b.innerText.toLowerCase();
                if (!isNaN(Number(A)) && !isNaN(Number(B))) {
                    if (Number(A) < Number(B)) return -1;
                    if (Number(A) > Number(B)) return 1;
                } else {
                    if (A < B) return -1;
                    if (A > B) return 1;
                }
                return 0;
            }).map(function (td) {
                return _this.dropdownFilterItem(td, self);
            });
            this.inputs = innerDivs.map(function (div) {
                return div.firstElementChild;
            });

            var selectAllCheckboxDiv = this.dropdownFilterItemSelectAll();
            this.selectAllCheckbox = selectAllCheckboxDiv.firstElementChild;
            innerDivs.unshift(selectAllCheckboxDiv);

            var searchFilterDiv = this.dropdownFilterSearch();
            this.searchFilter = searchFilterDiv.firstElementChild;

            var outerDiv = innerDivs.reduce(function (outerDiv, innerDiv) {
                outerDiv.appendChild(innerDiv);
                return outerDiv;
            }, document.createElement('div'));

            outerDiv.className = 'checkbox-container';

            var elements = [];

            if (this.options.sort) elements = elements.concat([this.dropdownFilterSort(this.options.captions.a_to_z), this.dropdownFilterSort(this.options.captions.z_to_a)]);
            if (this.options.search) elements.push(searchFilterDiv);
            return elements.concat(outerDiv).reduce(function (html, el) {
                html.appendChild(el);
                return html;
            }, dropdownFilterContent);
        };

        // 필터 선택 목록
        FilterMenu.prototype.dropdownFilterDropdown = function () {
            // 'div' 태그를 만들기
            var dropdownFilterDropdown = document.createElement('div');
            // 'div.dropdown-filter-dropdown' class name 주기
            dropdownFilterDropdown.className = 'dropdown-filter-dropdown';
            // arrow 변수 선언 - 'span' 태그
            var arrow = document.createElement('span');
            // span.glyphicon ~ class name 명시
            arrow.className = 'glyphicon glyphicon-arrow-down dropdown-filter-icon';
            // icon 변수 선언
            var icon = document.createElement('i');
            // 'i.arrow-down'
            icon.className = 'fas fa-fw fa-sort-down';
            // arrow html 요소에 icon을 붙이기
            arrow.appendChild(icon);
            // dropdownFilterDropdown 변수에 arrow html 붙이기
            dropdownFilterDropdown.appendChild(arrow);
            // dropdownFilterDropdown 변수에 이 변수의 dropdownFilterContent 붙이기
            dropdownFilterDropdown.appendChild(this.dropdownFilterContent());
            if ($(this.th).hasClass('no-sort')) {
                $(dropdownFilterDropdown).find('.dropdown-filter-sort').remove();
            }
            if ($(this.th).hasClass('no-filter')) {
                $(dropdownFilterDropdown).find('.checkbox-container').remove();
            }
            if ($(this.th).hasClass('no-search')) {
                $(dropdownFilterDropdown).find('.dropdown-filter-search').remove();
            }
            return dropdownFilterDropdown;
        };
        return FilterMenu;
    }();

    // FilterCollection 변수 선언
    var FilterCollection = function () {
        function FilterCollection(target, options) {
            this.target = target;
            this.options = options;
            this.ths = target.find('th' + options.columnSelector).toArray();
            this.filterMenus = this.ths.map(function (th, index) {
                var column = $(th).index();
                return new FilterMenu(target, th, column, index, options);
            });
            this.rows = target.find('tbody').find('tr').toArray();
            this.table = target.get(0);
        }

        // 초기값 설정
        FilterCollection.prototype.initialize = function () {
            this.filterMenus.forEach(function (filterMenu) {
                filterMenu.initialize();
            });
            this.bindCheckboxes();
            this.bindSelectAllCheckboxes();
            this.bindSort();
            this.bindSearch();
        };

        // 체크박스 바인딩
        FilterCollection.prototype.bindCheckboxes = function () {
            var filterMenus = this.filterMenus;
            var rows = this.rows;
            var ths = this.ths;
            var updateRowVisibility = this.updateRowVisibility;
            this.target.find('.dropdown-filter-menu-item.item').change(function () {
                var index = $(this).data('index');
                var value = $(this).val();
                filterMenus[index].updateSelectAll();
                updateRowVisibility(filterMenus, rows, ths);
            });
        };

        // 선택된 모든 체크박스 바인딩
        FilterCollection.prototype.bindSelectAllCheckboxes = function () {
            var filterMenus = this.filterMenus;
            var rows = this.rows;
            var ths = this.ths;
            var updateRowVisibility = this.updateRowVisibility;
            this.target.find('.dropdown-filter-menu-item.select-all').change(function () {
                var index = $(this).data('index');
                var value = this.checked;
                filterMenus[index].selectAllUpdate(value);
                updateRowVisibility(filterMenus, rows, ths);
            });
        };

        // 바인딩 정렬
        FilterCollection.prototype.bindSort = function () {
            var filterMenus = this.filterMenus;
            var rows = this.rows;
            var ths = this.ths;
            var sort = this.sort;
            var table = this.table;
            var options = this.options;
            var updateRowVisibility = this.updateRowVisibility;
            this.target.find('.dropdown-filter-sort').click(function () {
                var $sortElement = $(this).find('span');
                var column = $sortElement.data('column');
                var order = $sortElement.attr('class');
                sort(column, order, table, options);
                updateRowVisibility(filterMenus, rows, ths);
            });
        };

        // 바인딩 검색
        FilterCollection.prototype.bindSearch = function () {
            var filterMenus = this.filterMenus;
            var rows = this.rows;
            var ths = this.ths;
            var updateRowVisibility = this.updateRowVisibility;
            this.target.find('.dropdown-filter-search').keyup(function () {
                console.log('dropdown seaching is working!')
                var $input = $(this).find('input');
                var index = $input.data('index');
                var value = $input.val();
                filterMenus[index].searchToggle(value);
                updateRowVisibility(filterMenus, rows, ths);
            });
        };

        // 레코드 display update
        FilterCollection.prototype.updateRowVisibility = function (filterMenus, rows, ths) {
            var showRows = rows;
            var hideRows = [];
            var selectedLists = filterMenus.map(function (filterMenu) {
                return {
                    column: filterMenu.column,
                    selected: filterMenu.inputs.filter(function (input) {
                        return input.checked;
                    }).map(function (input) {
                        return input.value.trim().replace(/ +(?= )/g, '');
                    })
                };
            });
            for (var i = 0; i < rows.length; i++) {
                var tds = rows[i].children;
                for (var j = 0; j < selectedLists.length; j++) {
                    var content = tds[selectedLists[j].column].innerText.trim().replace(/ +(?= )/g, '');
                    if (selectedLists[j].selected.indexOf(content) === -1) {
                        $(rows[i]).hide();
                        break;
                    }
                    $(rows[i]).show();
                }
            }
            // $(rows).filter(function () {
            //     var showRow = false;
            //
            //     var tds = this.children;
            //     for (var j = 0; j < selectedLists.length; j++) {
            //     //var content = tds[selectedLists[j].column].innerText.trim().replace(/ +(?= )/g, '');
            //         var content = $(tds[selectedLists[j].column]).text().trim();
            //         if (selectedLists[j].selected.indexOf(content) == -1) {
            //             showRow = false;
            //             break;
            //         }
            //
            //         showRow = true;
            //     }
            //     $(this).toggle(showRow);
            // })
        };

        // 정렬
        FilterCollection.prototype.sort = function (column, order, table, options) {
            var flip = 1;
            if (order === options.captions.z_to_a.toLowerCase().split(' ').join('-')) flip = -1;
            var tbody = $(table).find('tbody').get(0);
            var rows = $(tbody).find('tr').get();
            rows.sort(function (a, b) {
                var A = a.children[column].innerText.toUpperCase();
                var B = b.children[column].innerText.toUpperCase();
                if (!isNaN(Number(A)) && !isNaN(Number(B))) {
                    if (Number(A) < Number(B)) return -1 * flip;
                    if (Number(A) > Number(B)) return 1 * flip;
                } else {
                    if (A < B) return -1 * flip;
                    if (A > B) return 1 * flip;
                }
                return 0;
            });
            for (var i = 0; i < rows.length; i++) {
                tbody.appendChild(rows[i]);
            }
        };
        return FilterCollection;
    }();

    $$1.fn.excelTableFilter = function (options) {
        var target = this;
        options = $$1.extend({}, $$1.fn.excelTableFilter.options, options);
        if (typeof options.columnSelector === 'undefined') options.columnSelector = '';
        if (typeof options.sort === 'undefined') options.sort = true;
        if (typeof options.search === 'undefined') options.search = true;
        if (typeof options.captions === 'undefined') options.captions = {
            a_to_z: '오름차순',
            z_to_a: '내림차순',
            search: '검색',
            select_all: '모두 선택'
        };
        var filterCollection = new FilterCollection(target, options);
        filterCollection.initialize();
        return target;
    };
    $$1.fn.excelTableFilter.options = {};


}(jQuery));
//# sourceMappingURL=excel-bootstrap-table-filter-bundle.js.map