import arcpy
from agol_inventory import *



if __name__ == '__main__':
    
    # Get input parameters
    use_agol_default = arcpy.GetParameter(0)
    url = arcpy.GetParameterAsText(1)
    username = arcpy.GetParameterAsText(2)
    pw = arcpy.GetParameterAsText(3)
    depth = arcpy.GetParameterAsText(4)
    thread_count = int(arcpy.GetParameterAsText(5))
    output_excel = arcpy.GetParameter(6)
    output_excel_file =arcpy.GetParameterAsText(7)
    output_db = arcpy.GetParameter(8)
    output_db_file = arcpy.GetParameterAsText(9)

    # Session GIS
    if use_agol_default:
        session_gis = arcgis.gis.GIS("home")
    else:
        session_gis = arcgis.gis.GIS(url, username, pw)
    
    # Reformat the depth variable
    if depth == 'User':
        depth = 'user'
    elif depth == 'Organization':
        depth = 'org'
    elif depth == 'Extended':
        depth = 'extended'
    else:
        arcpy.AddError(f"Could not identify the depth values {depth}, please make sure this value is User, Organization, or Extended")


    try:
        # Run Functions
        inventory_dict = set_up_dict_lists()


        arcpy.AddMessage('Scanning Groups...')
        group_scan(session_gis, inventory_dict, thread_count)

        arcpy.AddMessage('Scanning Users...')
        folder_dict = user_scan(session_gis, inventory_dict, thread_count)

        arcpy.AddMessage('Scanning Items...')
        item_scan(session_gis, inventory_dict, folder_dict, thread_count)

        if output_excel:
            arcpy.AddMessage("Creating Excel Output File")
            output_to_excel(inventory_dict, output_excel_file)

        if output_db:
            arcpy.AddMessage("Creating SQLite Output File")
            output_to_sqlite(inventory_dict, output_db_file)
    except Exception as e:
        arcpy.AddError("There was an error running the inventory tool")
        arcpy.AddError(str(e))
    
    arcpy.AddMessage("Finished!")


    