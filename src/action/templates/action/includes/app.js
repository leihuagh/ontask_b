  $(document).ready(function() {
    var options ={
      plugins: ['bt-tooltip-errors', 'not-group'],
      allow_empty: true,
      filters: [{
        id: 'name',
        label: 'Name',
        type: 'string'
      }, {
        id: 'category',
        label: 'Category',
        type: 'integer',
        input: 'select',
        values: {
          1: 'Books',
          2: 'Movies',
          3: 'Music',
          4: 'Tools',
          5: 'Goodies',
          6: 'Clothes'
        },
        operators: ['equal', 'not_equal', 'in', 'not_in', 'is_null', 'is_not_null']
      }, {
        id: 'in_stock',
        label: 'In stock',
        type: 'integer',
        input: 'radio',
        values: {
          1: 'Yes',
          0: 'No'
        },
        operators: ['equal']
      }, {
        id: 'price',
        label: 'Price',
        type: 'double',
        validation: {
          min: 0,
          step: 0.01
        }
      }, {
        id: 'id',
        label: 'Identifier',
        type: 'string',
        placeholder: '____-____-____',
        operators: ['equal', 'not_equal'],
        validation: {
          format: /^.{4}-.{4}-.{4}$/
        }
      }],
//filters: [{id: 'SID', type: 'integer'},{id: 'email', type: 'string'},{id: 'Q01',
// type: 'double', validation: { step: 'any' }},{id: 'Q02', type: 'double', validation: { step: 'any' }}]
    }
    $('#builder').queryBuilder(options);

    $('.parse-json').on('click', function() {
      rules = $('#builder').queryBuilder('getRules');
      // rules = $('#builder').queryBuilder('getSQL');
      console.log('Rules: ' + rules);
      console.log(JSON.stringify(rules, undefined, 2));
     });
   });