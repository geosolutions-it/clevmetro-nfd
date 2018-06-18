/*
 * Copyright 2018, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

module.exports = {
    row: [
        {
            name: 'Natural Area Code',
            type: 'text',
            code: 'element_natural_area_code_nac',
            only: '/nfdapi/report_natural_area/'
        },
        {
            name: 'Rank',
            id: 'rank',
            desc: ['Name', 'Value'],
            type: ['select', 'text'],
            code: ['rank_name', 'rank_value'],
            url: '/nfdapi/taxon_ranks/',
            only: '/nfdapi/report_taxon/'
        },
        {
            name: 'Reservation',
            type: 'multiselect',
            url: '/nfdapi/reservation/',
            code: 'reservation'
        },
        {
            name: 'Watershed',
            type: 'multiselect',
            url: '/nfdapi/watershed/',
            code: 'watershed'
        },
        {
            name: 'County',
            type: 'text',
            code: 'county',
            only: '/nfdapi/report_taxon/'
        },
        {
            name: 'Quad',
            id: 'quad',
            desc: ['Name', 'Number'],
            type: ['text', 'number'],
            code: ['quad_name', 'quad_number'],
            only: '/nfdapi/report_taxon/'
        },
        {
            name: 'Global Status',
            type: 'multiselect',
            url: '/nfdapi/grank/',
            code: 'global_status'
        },
        {
            name: 'State Status',
            type: 'multiselect',
            url: '/nfdapi/srank/',
            code: 'state_status'
        },
        {
            name: 'CM Status',
            type: 'multiselect',
            url: '/nfdapi/cmstatus/',
            code: 'cm_status'
        },
        {
            name: 'Observer',
            type: 'text',
            code: 'observer'
        },
        {
            id: 'observation_date',
            name: 'Observation Date Range',
            type: 'date',
            code: ['observation_date_0', 'observation_date_1']
        }
    ],
    col: [
        {
            name: 'Field',
            type: 'checkbox',
            options: [
                {
                    name: 'List ID',
                    code: 'show_list_id'
                },
                {
                    name: 'DB ID',
                    code: 'show_db_id'
                },
                {
                    name: 'Genus',
                    code: 'show_genus'
                },
                {
                    name: 'Species',
                    code: 'show_species'
                },
                {
                    name: 'Common name',
                    code: 'show_common_name'
                },
                {
                    name: 'Natural Area Code',
                    code: 'show_natural_area_code'
                },
                {
                    name: 'Natural Area Description',
                    code: 'show_general_description'
                },
                {
                    name: 'Observation Date',
                    code: 'show_observation_date'
                },
                {
                    name: 'Observer name',
                    code: 'show_observer'
                },
                {
                    name: 'Site description',
                    code: 'show_site_description'
                },
                {
                    name: 'Reservation',
                    code: 'show_reservation'
                },
                {
                    name: 'Watershed',
                    code: 'show_watershed'
                },
                {
                    name: 'Global Status',
                    code: 'show_global_status'
                },
                {
                    name: 'Federal Status',
                    code: 'show_federal_status'
                },
                {
                    name: 'State Status',
                    code: 'show_state_status'
                },
                {
                    name: 'CM Status',
                    code: 'show_cm_status'
                },
                {
                    name: 'Latitude',
                    code: 'show_latitude'
                },
                {
                    name: 'Longitude',
                    code: 'show_longitude'
                }
            ]
        }
    ]
};
