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
                console.log('trigger is working!')
                return $content.toggle();
            });

            $(document).click(function (el) {
                if (!$menu.is(el.target) && $menu.has(el.target).length === 0) {
                    $content.hide();
                    console.log('------ here is >>> initialize ---------------')
                }
            });
        };

    }
}(jQuery));