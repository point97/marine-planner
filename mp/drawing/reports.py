# coding: utf-8
from general.utils import format_precision
from django.db.models import Q
from django.conf import settings
from django.db.models import Sum, Avg, Min, Max, Count


def get_min(grid_cells, field):
    grid_cells = remove_nulls(grid_cells, field)
    return grid_cells.aggregate(Min(field)).values()[0]

def get_max(grid_cells, field):
    grid_cells = remove_nulls(grid_cells, field)
    return grid_cells.aggregate(Max(field)).values()[0]

def get_mode(grid_cells, field):
    grid_cells = remove_nulls(grid_cells, field)
    try:
        mode = grid_cells.values(field).annotate(
            count=Count(field)).order_by('-count')[0][field]
    except IndexError:
        mode = None
    return mode

def get_range(grid_cells, field):
    return get_min(grid_cells, field), get_max(grid_cells, field)

def get_count_gt(grid_cells, field, gt_value):
    grid_cells = grid_cells.filter(Q((field + "__gt", gt_value)))
    count = grid_cells.count()
    return count

def get_count_eq(grid_cells, field, value):
    grid_cells = grid_cells.filter(Q((field, value)))
    count = grid_cells.count()
    return count

def get_count_notnull(grid_cells, field):
    grid_cells = remove_nulls(grid_cells, field)
    return grid_cells.count()

def get_sum(grid_cells, field):
    grid_cells = remove_nulls(grid_cells, field)
    return grid_cells.aggregate(Sum(field)).values()[0]

def remove_nulls(grid_cells, field):
    # Only compute averages on non-null cells
    return grid_cells.filter(~Q((field, settings.NULLVALUE)))

def get_average(grid_cells, field):
    grid_cells = remove_nulls(grid_cells, field)
    return grid_cells.aggregate(Avg(field)).values()[0]

def get_unique_values(grid_cells, field):
    values = []
    for gc in grid_cells:
        value = getattr(gc, field)
        if value not in values:
            values.append(value)
    return values


def header(h):
    return {'title': '<h4>{}</h4>'.format(h), 'data': ''}


def sefcri_area():
    """
    Instead of calculating this each time (4+ sec), we optimize through hardcoding
        from scenarios.models import GridCell
        region_area = sum([gc.geometry.area
            for gc in GridCell.objects.all()]) / 1000000  # m² to km²
        return region_area
    """
    return 1209.5066211463068  # km²


def total_reef_area():
    """
    Instead of calculating this each time (4+ sec), we optimize through hardcoding
        from scenarios.models import GridCell
        reef_area = get_sum(GridCell.objects.all(), 'reef_area')
        return reef_area
    """
    return 228508729  # m²


def get_summary_reports(grid_cells):
    """
    List of attributes for drawing summary reports
    """
    attributes = []

    if grid_cells.count() == 0:
        return attributes

    # ################################### Habitat ##############################
    attributes.append(header('HABITAT'))

    cell_count = grid_cells.count()
    attributes.append({'title': 'Total Number of Planning Units (PU)',
                       'data': format(cell_count, ',d')})

    selected_area = sum([gc.geometry.area for gc in grid_cells]) / 1000000  # m² to km²
    attributes.append({'title': 'Total Area',
                       'data': str(format_precision(selected_area, 2)) + ' km²'})

    title = "Percent Area to SEFCRI region"
    data = format_precision(selected_area / sefcri_area(), 1) * 100
    attributes.append({'title': title, 'data': str(data) + '%'})

    title = "Benthic Habitat Eco-subregion(s)"
    regions = get_unique_values(grid_cells, 'region')
    attributes.append({'title': title, 'data': ", ".join(regions)})

    counties = get_unique_values(grid_cells, 'county')
    if len(counties) == 1:
        attributes.append({'title': 'County', 'data': counties[0]})
    elif len(counties) > 1:
        attributes.append({'title': 'Counties', 'data': ", ".join(counties)})

    # Depth Range, no mean
    min_depth = get_min(grid_cells, 'depth_min')
    max_depth = get_max(grid_cells, 'depth_max')
    depth_range = '%s to %s feet' % (
        format_precision(min_depth, 0),
        format_precision(max_depth, 0))
    attributes.append({'title': 'Depth Range', 'data': depth_range})

    mean_depth = get_average(grid_cells, 'depth_mean')  # mean of mean depth?
    data = '%s feet' % (format_precision(mean_depth, 0))
    attributes.append({'title': 'Average Depth', 'data': data})

    min_distance_to_shore, max_distance_to_shore = get_range(
        grid_cells, 'shore_distance')
    distance_to_shore = '%s - %s miles' % (
        format_precision(min_distance_to_shore, 1),
        format_precision(max_distance_to_shore, 1))
    attributes.append({
        'title': 'Distance Range from Shore',
        'data': distance_to_shore})

    min_distance_to_inlet, max_distance_to_inlet = get_range(
        grid_cells, 'inlet_distance')
    distance_to_inlet = '%s - %s miles' % (
        format_precision(min_distance_to_inlet, 1),
        format_precision(max_distance_to_inlet, 1))
    attributes.append({
        'title': 'Distance Range from Coastal Inlet',
        'data': distance_to_inlet})

    attributes.extend(header('TESTING'))

    min_distance_to_outfall, max_distance_to_outfall = get_range(
        grid_cells, 'outfall_distance')
    distance_to_outfall = '%s - %s miles' % (
        format_precision(min_distance_to_outfall, 1),
        format_precision(max_distance_to_outfall, 1))
    attributes.append({
        'title': 'Distance Range from Outfall',
        'data': distance_to_outfall})

    min_distance_to_pier, max_distance_to_pier = get_range(
        grid_cells, 'pier_distance')
    distance_to_pier = '%s - %s miles' % (
        format_precision(min_distance_to_pier, 1),
        format_precision(max_distance_to_pier, 1))
    attributes.append({
        'title': 'Distance Range from Pier',
        'data': distance_to_pier})

    title = "Planning units that contain Reef habitat"
    data = get_count_gt(grid_cells, 'reef_area', 0)
    attributes.append({'title': title, 'data': str(data)})

    title = 'Mapped Reef Habitat Area'
    area = get_sum(grid_cells, 'reef_area')
    data = str(format_precision(area, 0)) + ' m²'
    attributes.append({'title': title, 'data': data})

    title = "Planning units that contain Sand habitat"
    data = get_count_gt(grid_cells, 'sand_area', 0)
    attributes.append({'title': title, 'data': str(data)})

    title = 'Mapped Sand Habitat Area'
    area = get_sum(grid_cells, 'sand_area')
    data = str(format_precision(area, 0)) + ' m²'
    attributes.append({'title': title, 'data': data})

    title = "Planning units that contain Seagrass habitat"
    data = get_count_gt(grid_cells, 'sg_area', 0)
    attributes.append({'title': title, 'data': str(data)})

    title = 'Mapped Seagrass Habitat Area'
    area = get_sum(grid_cells, 'sg_area')
    data = str(format_precision(area, 0)) + ' m²'
    attributes.append({'title': title, 'data': data})

    title = "Planning units that contain Artificial Substrate habitat"
    data = get_count_gt(grid_cells, 'art_area', 0)
    attributes.append({'title': title, 'data': str(data)})

    title = 'Mapped Artificial Habitat Area'
    art_area = get_sum(grid_cells, 'art_area')
    data = str(format_precision(art_area, 0)) + ' m²'
    attributes.append({'title': title, 'data': data})

    title = 'Sponge Percent Cover Planning Units'
    val = get_count_notnull(grid_cells, 'sponge')
    attributes.append({'title': title, 'data': str(int(val))})
    title = 'Sponge Percent Cover Range'
    data = "%s - %s" % get_range(grid_cells, 'sponge')
    attributes.append({'title': title, 'data': data})
    title = 'Sponge Percent Cover Average'
    val = get_average(grid_cells, 'sponge')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})
    title = "Sponge Percent Cover Mode"
    val = get_mode(grid_cells, 'sponge')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})

    # ################################### Coral ##############################
    attributes.append(header('CORAL'))

    title = 'Planning Units containing Coral Density Surveys'
    val = get_count_notnull(grid_cells, 'coral_density')
    attributes.append({'title': title, 'data': str(int(val))})
    title = 'Coral Density (corals per m²) Range'
    data = "%s - %s" % get_range(grid_cells, 'coral_density')
    attributes.append({'title': title, 'data': data})
    title = 'Coral Density (corals per m²) Average'
    coral_density = get_average(grid_cells, 'coral_density')
    data = str(format_precision(coral_density, 0))
    attributes.append({'title': title, 'data': data})
    title = "Coral Density (corals per m²) Mode"
    val = get_mode(grid_cells, 'coral_density')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})

    title = 'Planning Units containing Coral Percent Cover Surveys'
    val = get_count_notnull(grid_cells, 'coral_cover')
    attributes.append({'title': title, 'data': str(int(val))})
    title = 'Coral Percent Cover Range'
    data = "%s - %s" % get_range(grid_cells, 'coral_cover')
    attributes.append({'title': title, 'data': data})
    title = 'Coral Percent Cover Average'
    coral_cover = get_average(grid_cells, 'coral_cover')
    data = str(format_precision(coral_cover, 0))
    attributes.append({'title': title, 'data': data})
    title = "Coral Percent Cover Mode"
    val = get_mode(grid_cells, 'coral_cover')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})

    title = 'Planning Units containing Number of Coral Species Surveys'
    val = get_count_notnull(grid_cells, 'coral_richness')
    attributes.append({'title': title, 'data': str(int(val))})
    title = 'Number of Coral Species Range'
    data = "%s - %s" % get_range(grid_cells, 'coral_richness')
    attributes.append({'title': title, 'data': data})
    title = 'Number of Coral Species Average'
    coral_richness = get_average(grid_cells, 'coral_richness')
    data = str(format_precision(coral_richness, 0))
    attributes.append({'title': title, 'data': data})
    title = "Number of Coral Species Mode"
    val = get_mode(grid_cells, 'coral_richness')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})

    title = 'Large Live Coral Planning Units'
    num_large_live_corals = get_count_eq(grid_cells, 'large_live_coral', 'Y')
    data = str(num_large_live_corals)
    attributes.append({'title': title, 'data': data})

    title = 'Dense Acropora Patch Planning Units'
    num_acropora = get_count_eq(grid_cells, 'acropora_pa', 'Y')
    data = str(num_acropora)
    attributes.append({'title': title, 'data': data})

    title = 'Mapped Dense Acropora cervicornis Habitat Area'
    acerv_area = get_sum(grid_cells, 'acerv_area')
    data = str(format_precision(acerv_area, 0)) + ' m²'
    attributes.append({'title': title, 'data': data})

    title = 'Pillar Coral Planning Units'
    num_pillar_presence = get_count_eq(grid_cells, 'pillar_presence', 'P')
    data = str(num_pillar_presence)
    attributes.append({'title': title, 'data': data})

    title = 'Planning Units containing Bleached Coral'
    count = get_count_gt(grid_cells, 'coral_bleach', 0)
    pct = format_precision(count / cell_count, 2)
    attributes.append({'title': title, 'data': str(count)})
    attributes.append({'title': "Percentage of " + title, 'data': str(pct)})

    title = 'Planning Units containing Diseased Coral'
    count = get_count_gt(grid_cells, 'coral_disease', 0)
    data = format_precision(count / cell_count, 2)
    attributes.append({'title': title, 'data': str(count)})
    attributes.append({'title': "Percentage of " + title, 'data': str(pct)})

    title = 'Coral Resilience Index Planning Units (FRRP)'
    count = get_count_notnull(grid_cells, 'coral_resilience')
    attributes.append({'title': title, 'data': str(data)})

    title = 'Soft Coral Percent Cover Planning Units'
    val = get_count_notnull(grid_cells, 'coral_soft')
    attributes.append({'title': title, 'data': str(int(val))})
    title = 'Soft Coral Percent Cover Range'
    data = "%s - %s" % get_range(grid_cells, 'coral_soft')
    attributes.append({'title': title, 'data': data})
    title = 'Soft Coral Percent Cover Average'
    val = get_average(grid_cells, 'coral_soft')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})
    title = "Soft Coral Percent Cover Mode"
    val = get_mode(grid_cells, 'coral_soft')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})

    # ################################### Fish ##############################
    attributes.append(header('FISH'))

    title = 'Reef Fish Density Planning Units'
    val = get_count_notnull(grid_cells, 'reef_fish_density')
    attributes.append({'title': title, 'data': str(int(val))})
    title = 'Reef Fish Density Range'
    data = "%s - %s" % get_range(grid_cells, 'reef_fish_density')
    attributes.append({'title': title, 'data': data})
    title = 'Reef Fish Density Average'
    val = get_average(grid_cells, 'reef_fish_density')
    data = str(format_precision(val, 1)) + ' '
    attributes.append({'title': title, 'data': data})
    title = "Reef Fish Density Mode"
    val = get_mode(grid_cells, 'reef_fish_density')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})

    title = 'Number of Reef Fish Species Planning Units'
    val = get_count_notnull(grid_cells, 'reef_fish_richness')
    attributes.append({'title': title, 'data': str(int(val))})
    title = 'Number of Reef Fish Species Range'
    data = "%s - %s" % get_range(grid_cells, 'reef_fish_richness')
    attributes.append({'title': title, 'data': data})
    title = 'Number of Reef Fish Species Average'
    val = get_average(grid_cells, 'reef_fish_richness')
    data = str(format_precision(val, 1)) + ''
    attributes.append({'title': title, 'data': data})
    title = 'Number of Reef Fish Species Mode'
    val = get_mode(grid_cells, 'reef_fish_richness')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})

    title = 'Recreationally and Commercially Important Fishes Planning Units'
    val = get_count_notnull(grid_cells, 'reccom_fish')
    attributes.append({'title': title, 'data': str(int(val))})
    title = 'Recreationally and Commercially Important Fish Density Range'
    data = "%s - %s" % get_range(grid_cells, 'reccom_fish')
    attributes.append({'title': title, 'data': data})
    title = 'Recreationally and Commercially Important Fish Density Average'
    val = get_average(grid_cells, 'reccom_fish')
    data = str(format_precision(val, 1)) + ''
    attributes.append({'title': title, 'data': data})
    title = 'Recreationally and Commercially Important Fish Density Mode'
    val = get_mode(grid_cells, 'reccom_fish')
    data = str(format_precision(val, 0))
    attributes.append({'title': title, 'data': data})

    # ################################### People ##############################
    attributes.append(header('People'))

    title = 'Total Use Intensity (OFR 2015)'
    val = get_sum(grid_cells, 'sum_all')
    data = str(format_precision(val, 0)) + ' activity days'
    attributes.append({'title': title, 'data': data})

    title = 'Boater Use Intensity (OFR 2015)'
    val = get_sum(grid_cells, 'sum_boat')
    data = str(format_precision(val, 0)) + ' activity days'
    attributes.append({'title': title, 'data': data})

    title = 'Recreational Fishing Use Intensity (OFR 2015)'
    val = get_sum(grid_cells, 'sum_rec')
    data = str(format_precision(val, 0)) + ' activity days'
    attributes.append({'title': title, 'data': data})

    title = 'Scuba Diving Use Intensity (OFR 2015)'
    val = get_sum(grid_cells, 'sum_scuba')
    data = str(format_precision(val, 0)) + ' activity days'
    attributes.append({'title': title, 'data': data})

    title = 'Extractive Diving Use Intensity (OFR 2015)'
    val = get_sum(grid_cells, 'sum_extdive')
    data = str(format_precision(val, 0)) + ' activity days'
    attributes.append({'title': title, 'data': data})

    title = 'Spearfishing Use Intensity (OFR 2015)'
    val = get_sum(grid_cells, 'sum_spear')
    data = str(format_precision(val, 0)) + ' activity days'
    attributes.append({'title': title, 'data': data})

    title = 'Water Sports Use Intensity (OFR 2015)'
    val = get_sum(grid_cells, 'sum_watersport')
    data = str(format_precision(val, 0)) + ' activity days'
    attributes.append({'title': title, 'data': data})

    title = 'Diving and Fishing Use Overlap Planning Units'
    data = get_count_notnull(grid_cells, 'divefish_overlap')
    attributes.append({'title': title, 'data': str(data)})

    title = "Anchoring Density Planning Units (Berhinger data)"
    levels = ['Low', 'Medium', 'High', 'Very High']
    for level in levels:
        data = get_count_eq(grid_cells, 'anchor_desc', level)
        attributes.append({
            'title': title + ": " + level,
            'data': str(data)})

    title = 'Anchorage Area Planning Units'
    data = get_count_eq(grid_cells, 'anchorage', 'Y')
    attributes.append({'title': title, 'data': str(data)})

    title = "Mooring Density Planning Units (Berhinger data)"
    levels = ['Low', 'Medium', 'High', 'Very High']
    for level in levels:
        data = get_count_eq(grid_cells, 'mooring_desc', level)
        attributes.append({
            'title': title + ": " + level,
            'data': str(data)})

    title = 'Mooring Buoy Planning Units'
    data = get_count_eq(grid_cells, 'mooring_buoy', 'Y')
    attributes.append({'title': title, 'data': str(data)})

    title = 'Injury Site Planning Units'
    data = get_count_eq(grid_cells, 'injury_site', 'Y')
    attributes.append({'title': title, 'data': str(data)})

    title = 'Historic Impacts Planning Units'
    data = get_count_eq(grid_cells, 'impacted', 'Y')
    attributes.append({'title': title, 'data': str(data)})

    return attributes


def get_chart_values(uid, grid_cells):
    selected_area = sum([gc.geometry.area for gc in grid_cells])  # m2
    selected_reef_area = get_sum(grid_cells, 'reef_area')
    if not selected_reef_area:
        selected_reef_area = 0
    selected_sand_area = get_sum(grid_cells, 'sand_area')
    if not selected_sand_area:
        selected_sand_area = 0
    fish_species = get_max(grid_cells, 'reef_fish_richness')
    coral_species = get_max(grid_cells, 'coral_richness')
    min_depth = get_min(grid_cells, 'depth_min')
    max_depth = get_max(grid_cells, 'depth_max')
    min_diving, max_diving = get_range(grid_cells, 'sum_scuba')
    min_fishing, max_fishing = get_range(grid_cells, 'sum_rec')
    min_total, max_total = get_range(grid_cells, 'sum_all')
    all_reef_area = total_reef_area()
    chart_values = {
        'pct_reef': {
            'min': 0,
            'max': format_precision(100 * (selected_reef_area / selected_area)),
            'selection_id': uid},
        'pct_sand': {
            'min': 0,
            'max': format_precision(100 * (selected_sand_area / selected_area)),
            'selection_id': uid},
        'pct_reef_total': {
            'min': 0,
            'max': format_precision(100 * (float(selected_reef_area) / all_reef_area)),
            'selection_id': uid},
        'fish_species': {
            'min': 0,
            'max': fish_species,
            'selection_id': uid},
        'coral_species': {
            'min': 0,
            'max': coral_species,
            'selection_id': uid},
        'diving': {
            'min': min_diving,
            'max': max_diving,
            'selection_id': uid},
        'fishing': {
            'min': min_fishing,
            'max': max_fishing,
            'selection_id': uid},
        'total': {
            'min': min_total,
            'max': max_total,
            'selection_id': uid},
        'depth': {
            'min': min_depth,
            'max': max_depth,
            'selection_id': uid},
    }
    return chart_values
