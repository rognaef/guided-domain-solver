import json


def parse_stackup_to_graph(json_file_path, graph):
    """Parse the stackup section from JSON file and create nodes and relationships in Neo4j."""
    try:
        # Load JSON data
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Helper function to get standardized layer name from layer number
        def get_layer_name(layer_number):
            return f'Layer{layer_number}'

        # Helper function to get origin_z variable name for a layer
        def get_origin_z_name(layer_number):
            return f'origin_z_{get_layer_name(layer_number)}'

        def get_thickness_name(layer_number):
            return f'thickness_{get_layer_name(layer_number)}'

        # Access the stackup data
        stackup_data = data.get('stackup', {})

        # Create a node for the stackup itself
        create_stackup_node = """
        CREATE (s:Stackup {name: 'Stackup', category: 'stackup'})
        """
        graph.query(create_stackup_node)

        # Parse soldermask if it exists
        if 'soldermask' in stackup_data:
            sm_data = stackup_data['soldermask']

            # Create soldermask node
            create_sm_node = """
            CREATE (sm:Soldermask {
                name: 'Soldermask',
                smthickness: $smthickness,
                smdf: $smdf,
                smdk: $smdk,
                category: 'soldermask'
            })
            WITH sm
            MATCH (s:Stackup {name: 'Stackup'})
            CREATE (s)-[:HAS_SOLDERMASK]->(sm)
            """
            graph.query(create_sm_node, {
                'smthickness': sm_data.get('smthickness', ''),
                'smdf': sm_data.get('smdf', ''),
                'smdk': sm_data.get('smdk', '')
            })

            # Create thickness variable node for soldermask
            create_sm_thickness = """
            CREATE (t:Variable {
                name: 'soldermask_thickness',
                value: $value,
                category: 'variable'
            })
            WITH t
            MATCH (sm:Soldermask {name: 'Soldermask'})
            CREATE (sm)-[:THICKNESS]->(t)
            """
            graph.query(create_sm_thickness, {'value': sm_data.get('smthickness', '')})

        # Parse layers
        # Store layer numbers to order them properly later
        layer_numbers = []

        # Note: We are only parsing keys that exactly match "layerX" pattern
        # and intentionally skipping "layermanrules", "vias", and "extinfo"
        for layer_key in stackup_data:
            if layer_key.startswith('layer') and layer_key != 'layermanrules':
                layer_data = stackup_data[layer_key]
                layer_number = layer_key[5:]  # Extract number from "layerX"

                # Use the helper function to get layer name and thickness name
                layer_name = get_layer_name(layer_number)
                thickness_name = get_thickness_name(layer_number)

                # Add layer number to our tracking list
                if layer_number.isdigit():
                    layer_numbers.append(int(layer_number))

                # Get material properties
                original_material_name = layer_data.get('material', '')
                paramdf = layer_data.get('paramdf', '')
                paramdk = layer_data.get('paramdk', '')

                # If material is "Other" or any non-specific name, find or create a material based on properties
                if original_material_name == "Other":
                    # Check if a material with the same properties already exists
                    find_material = """
                    MATCH (m:Material)
                    WHERE m.paramdf = $paramdf AND m.paramdk = $paramdk AND m.name STARTS WITH 'Material'
                    RETURN m.name AS name LIMIT 1
                    """
                    result = graph.query(find_material, {
                        'paramdf': paramdf,
                        'paramdk': paramdk
                    })

                    if result:
                        # Use existing material
                        material_name = result[0]['name']
                    else:
                        # Create new material with indexed name
                        get_next_idx = """
                        MATCH (m:Material)
                        WHERE m.name STARTS WITH 'Material' AND substring(m.name, 8) =~ '^[0-9]+$'
                        RETURN
                            CASE
                                WHEN COUNT(m) = 0 THEN 1
                                ELSE toInteger(MAX(substring(m.name, 8))) + 1
                            END as next_idx
                        """
                        idx_result = graph.query(get_next_idx)
                        next_idx = idx_result[0]['next_idx'] if idx_result else 1

                        material_name = f"Material{next_idx}"

                        # Create new material node
                        create_material = """
                        CREATE (m:Material {
                            name: $name,
                            paramdf: $paramdf,
                            paramdk: $paramdk,
                            category: 'material'
                        })
                        """
                        graph.query(create_material, {
                            'name': material_name,
                            'paramdf': paramdf,
                            'paramdk': paramdk
                        })
                else:
                    # For named materials (e.g. "Copper"), use the original name
                    material_name = original_material_name

                    # Create or update the material node
                    create_material = """
                    MERGE (m:Material {name: $name})
                    ON CREATE SET
                        m.paramdf = $paramdf,
                        m.paramdk = $paramdk,
                        m.category = 'material'
                    """
                    graph.query(create_material, {
                        'name': material_name,
                        'paramdf': paramdf,
                        'paramdk': paramdk
                    })

                # Create thickness variable node
                thickness_value = layer_data.get('thickness', '')
                create_thickness_node = """
                CREATE (t:Variable {
                    name: $name,
                    value: $value,
                    category: 'variable'
                })
                """
                graph.query(create_thickness_node, {
                    'name': thickness_name,
                    'value': thickness_value
                })

                # Create layer node with required properties - origin_z will be set later
                create_layer_node = """
                CREATE (l:Layer {
                    name: $name,
                    type: $type,
                    gndl: $gndl,
                    pwrl: $pwrl,
                    index: $index,
                    thickness: $thickness,
                    category: 'layer'
                })
                WITH l
                MATCH (s:Stackup {name: 'Stackup'})
                CREATE (s)-[:HAS_LAYER]->(l)
                """
                graph.query(create_layer_node, {
                    'name': layer_name,
                    'type': layer_data.get('type', ''),
                    'gndl': layer_data.get('gndl', False),
                    'pwrl': layer_data.get('pwrl', False),
                    'index': int(layer_number) if layer_number.isdigit() else layer_number,
                    'thickness': thickness_name
                })

                # Connect layer to material
                connect_layer_material = """
                MATCH (l:Layer {name: $layer_name})
                MATCH (m:Material {name: $material_name})
                CREATE (l)-[:MATERIAL]->(m)
                """
                graph.query(connect_layer_material, {
                    'layer_name': layer_name,
                    'material_name': material_name
                })

                # Connect layer to thickness
                connect_layer_thickness = """
                MATCH (l:Layer {name: $layer_name})
                MATCH (t:Variable {name: $thickness_name})
                CREATE (l)-[:THICKNESS]->(t)
                """
                graph.query(connect_layer_thickness, {
                    'layer_name': layer_name,
                    'thickness_name': thickness_name
                })

        # After all layers are created, calculate and set origin_z properties based on layer order
        if layer_numbers:
            # Sort layer numbers to ensure proper order
            layer_numbers.sort()

            # Create origin_z node for the first layer
            first_layer = layer_numbers[0]
            first_layer_name = get_layer_name(first_layer)
            origin_name = get_origin_z_name(first_layer)

            create_first_layer_origin = """
            MATCH (l:Layer {name: $layer_name})-[:THICKNESS]->(t:Variable)
            CREATE (o:Variable {
                name: $origin_name,
                value: t.value,
                category: 'variable'
            })
            WITH l, o
            CREATE (l)-[:ORIGIN_Z]->(o)
            """
            graph.query(create_first_layer_origin, {
                'layer_name': first_layer_name,
                'origin_name': origin_name
            })

            # Create origin_z for subsequent layers
            for i in range(1, len(layer_numbers)):
                current_layer = layer_numbers[i]
                previous_layer = layer_numbers[i-1]

                current_layer_name = get_layer_name(current_layer)
                previous_layer_name = get_layer_name(previous_layer)
                current_origin_name = get_origin_z_name(current_layer)

                create_layer_origin = """
                MATCH (prev:Layer {name: $prev_name})-[:ORIGIN_Z]->(prev_o:Variable),
                      (prev:Layer {name: $prev_name})-[:THICKNESS]->(prev_t:Variable),
                      (curr:Layer {name: $curr_name})
                CREATE (o:Variable {
                    name: $origin_name,
                    value: toFloat(prev_o.value) + toFloat(prev_t.value),
                    category: 'variable'
                })
                WITH curr, o
                CREATE (curr)-[:ORIGIN_Z]->(o)
                """
                graph.query(create_layer_origin, {
                    'prev_name': previous_layer_name,
                    'curr_name': current_layer_name,
                    'origin_name': current_origin_name
                })

                # Create ORIGIN_COMPONENT relationships to track composition
                create_origin_components = """
                MATCH (l:Layer {name: $curr_name})-[:ORIGIN_Z]->(o:Variable),
                      (prev_l:Layer {name: $prev_name})-[:ORIGIN_Z]->(prev_o:Variable),
                      (prev_l)-[:THICKNESS]->(prev_t:Variable)
                CREATE (o)-[:ORIGIN_COMPONENT {order: 1}]->(prev_o)
                CREATE (o)-[:ORIGIN_COMPONENT {order: 2}]->(prev_t)
                """
                graph.query(create_origin_components, {
                    'curr_name': f'Layer{current_layer}',
                    'prev_name': f'Layer{previous_layer}'
                })

                # Connect layer to material
                connect_layer_material = """
                MATCH (l:Layer {name: $layer_name})
                MATCH (m:Material {name: $material_name})
                CREATE (l)-[:MATERIAL]->(m)
                SET l.material = $material_name
                """
                graph.query(connect_layer_material, {
                    'layer_name': layer_name,
                    'material_name': material_name
                })

            for layer_num in layer_numbers:
                update_layer = """
                MATCH (l:Layer {name: $layer_name})
                SET l.origin_z = $origin_z
                """
                graph.query(update_layer, {
                    'layer_name': get_layer_name(layer_num),
                    'origin_z': get_origin_z_name(layer_num)
                })

                add_code = """
                MATCH (l:Layer {name: $layer_name})
                MATCH (l)-[:ORIGIN_Z]->(oz:Variable)
                MATCH (l)-[:THICKNESS]->(t:Variable)
                MATCH (l)-[:MATERIAL]->(m:Material)
                WITH l,
                    oz.value AS origin_z_value,
                    oz.name AS origin_z_name,
                    t.value AS thickness_value,
                    t.name AS thickness_name,
                    l.name AS name,
                    m.name AS material_name
                SET l.code =
                    "origin = [0,0,'" + origin_z_name + "']\n" +
                    "thickness = '" + thickness_name + "'\n" +
                    "name = '" + name + "'\n" +
                    "material = '" + material_name + "'\n" +
                    "ansys.aedt.core.modeler.create_box(origin=origin, " +
                    "thickness=thickness, "+
                    "name=name, " +
                    "material=material) ",
                    l.material = material_name
                """
                graph.query(add_code, {
                    'layer_name': get_layer_name(layer_num)
                })

        # Parse vias
        if 'vias' in stackup_data:
            vias_data = stackup_data['vias']

            # First create copper material node if it doesn't exist (default material for vias)
            create_copper_material = """
            MERGE (m:Material {name: 'Copper', category: 'material'})
            """
            graph.query(create_copper_material)

            for via_key, via_data in vias_data.items():
                # Parse start and end layer indices from the "starttoendl" field
                start_end = via_data.get('starttoendl', '').split('-')
                start_layer = start_end[0] if len(start_end) > 0 else ''
                end_layer = start_end[1] if len(start_end) > 1 else ''

                # Create via node with these values
                create_via_node = """
                CREATE (v:Via {
                    name: $name,
                    start_layer: $start_layer,
                    end_layer: $end_layer,
                    drill: $drill,
                    plated: $plated,
                    adddrill: $adddrill,
                    dbdrill: $dbdrill,
                    stubl: $stubl,
                    remarks: $remarks,
                    via_type: $via_type,
                    category: 'via'
                })
                WITH v
                MATCH (s:Stackup {name: 'Stackup'})
                CREATE (s)-[:HAS_VIA]->(v)
                """
                graph.query(create_via_node, {
                    'name': via_key,
                    'start_layer': start_layer,
                    'end_layer': end_layer,
                    'drill': via_data.get('drill', ''),
                    'plated': via_data.get('plated', ''),
                    'adddrill': via_data.get('adddrill', False),
                    'dbdrill': via_data.get('dbdrill', ''),
                    'stubl': via_data.get('stubl', ''),
                    'remarks': via_data.get('remarks', ''),
                    'via_type': via_data.get('via_type', '')
                    # Removed material, start_position, end_position from direct properties
                })

                # Connect via to material (use specified material or default to Copper)
                connect_via_material = """
                MATCH (v:Via {name: $via_name})
                MATCH (m:Material {name: $material_name})
                CREATE (v)-[:MATERIAL]->(m)
                """
                graph.query(connect_via_material, {
                    'via_name': via_key,
                    'material_name': via_data.get('material', 'Copper')
                })

                # Connect via to material (use specified material or default to Copper)
                connect_via_material = """
                MATCH (v:Via {name: $via_name})
                MATCH (m:Material {name: $material_name})
                CREATE (v)-[:MATERIAL]->(m)
                """
                graph.query(connect_via_material, {
                    'via_name': via_key,
                    'material_name': via_data.get('material', 'Copper')
                })

                # Connect via to its start and end layers and position nodes
                if start_layer and end_layer:
                    connect_via_layers = """
                    MATCH (v:Via {name: $via_name})
                    MATCH (start:Layer {name: $start_layer_name})-[:ORIGIN_Z]->(start_o:Variable)
                    MATCH (end:Layer {name: $end_layer_name})-[:ORIGIN_Z]->(end_o:Variable)
                    CREATE (v)-[:STARTS_AT]->(start)
                    CREATE (v)-[:ENDS_AT]->(end)
                    CREATE (v)-[:START_POSITION]->(start_o)
                    CREATE (v)-[:END_POSITION]->(end_o)
                    """
                    graph.query(connect_via_layers, {
                        'via_name': via_key,
                        'start_layer_name': get_layer_name(start_layer),
                        'end_layer_name': get_layer_name(end_layer)
                    })

                # Generate code for via creation using the relationships rather than properties
                add_code = """
                MATCH (v:Via {name: $via_name})
                MATCH (v)-[:START_POSITION]->(start_o:Variable)
                MATCH (v)-[:END_POSITION]->(end_o:Variable)
                MATCH (v)-[:MATERIAL]->(m:Material)
                WITH v,
                    start_o.name AS start_position_name,
                    end_o.name AS end_position_name,
                    v.name AS name,
                    m.name AS material_name,
                    v.drill AS drill
                SET v.code =
                    "origin = [0,0,'" + start_position_name + "']\n" +
                    "height = -('" + end_position_name + "'-'" + start_position_name + "')\n" +
                    "radius = '" + drill + "'/2\n" +
                    "material = '" + material_name + "'\n" +
                    "name = '" + name + "'\n" +
                    "cylinder_object = ansys.aedt.core.modeler.create_cylinder(" +
                    "orientation='Z', " +
                    "origin=origin, " +
                    "radius=radius, " +
                    "height=height, " +
                    "name=name, " +
                    "material=material)"
                """
                graph.query(add_code, {
                    'via_name': via_key
                })

        # Parse layermanrules if it exists
        if 'layermanrules' in stackup_data:
            rules_data = stackup_data['layermanrules']

            # Create layermanrules node
            create_rules_node = """
            CREATE (r:LayerManRules {
                name: 'LayerManRules',
                minlinew: $minlinew,
                mingap: $mingap,
                minviadia: $minviadia,
                minviad: $minviad,
                mincatchd: $mincatchd,
                mindmetz: $mindmetz,
                pmetz: $pmetz,
                category: 'rules'
            })
            WITH r
            MATCH (s:Stackup {name: 'Stackup'})
            CREATE (s)-[:HAS_RULES]->(r)
            """
            graph.query(create_rules_node, {
                'minlinew': rules_data.get('minlinew', ''),
                'mingap': rules_data.get('mingap', ''),
                'minviadia': rules_data.get('minviadia', ''),
                'minviad': rules_data.get('minviad', ''),
                'mincatchd': rules_data.get('mincatchd', ''),
                'mindmetz': rules_data.get('mindmetz', ''),
                'pmetz': rules_data.get('pmetz', '')
            })

        # Parse extinfo if it exists
        if 'extinfo' in stackup_data:
            extinfo_data = stackup_data['extinfo']

            # Create extinfo node
            create_extinfo_node = """
            CREATE (e:ExtInfo {
                name: 'ExtInfo',
                value: $value,
                category: 'extinfo'
            })
            WITH e
            MATCH (s:Stackup {name: 'Stackup'})
            CREATE (s)-[:HAS_EXTINFO]->(e)
            """
            graph.query(create_extinfo_node, {
                'value': extinfo_data
            })

        print("Graph creation completed: Stackup structure imported into Neo4j")

    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{json_file_path}'.")
    except Exception as e:
        print(f"Error while parsing stackup: {type(e).__name__}: {e}")

    return graph
