from random import randrange

# init
relax_time = 1
vertices_number = 100
branches_number = 10
max_ticks = 100

output_vertex = {
    '.': vertices_number - 1,
    '0': vertices_number - 2,
    '1': vertices_number - 3,
    '2': vertices_number - 4,
    '3': vertices_number - 5,
    '4': vertices_number - 6,
    '5': vertices_number - 7,
    '6': vertices_number - 8,
    '7': vertices_number - 9,
    '8': vertices_number - 10,
    '9': vertices_number - 11
}

input_vertex = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8
}

start_hidden_vertex = 9
end_hidden_vertex = vertices_number - 11

vertices = [0 for i in range(vertices_number)]

# edges = [[0,2],[3,4]]
edges = []

# train data
train = [
    ['1', '1'],
    ['2', '1.414213562373095048801688724209698078569671875376'],
    ['3', '1.732050807568877293527446341505872366942805253810'],
    ['4', '2'],
    ['5', '2.236067977499789696409173668731276235440618359611'],
    ['6', '2.449489742783178098197284074705891391965947480656'],
    ['7', '2.645751311064590590501615753639260425710259183082'],
    ['8', '2.828427124746190097603377448419396157139343750753'],
    ['9', '3'],
]

# waves [
#     [1,2,4,5]
#  ]


symbol = 0
for sample in train:
    print('sample', sample[0])
    input_symbol_index = input_vertex[sample[0]]
    output_symbol_index = output_vertex[sample[1][0]]


    waves = []
    vertices = [0 for i in range(vertices_number)]

    found_path = False
    for tick in range(1, max_ticks):
        if found_path:
            break
        if tick == 1:
            # start the first wave
            rand_branches = [randrange(start_hidden_vertex, vertices_number) for i in range(branches_number)]
            for w in rand_branches:
                # reach the end
                if w == output_symbol_index:
                    found_path = True
                    print("founded for ", sample[0], "tick ", tick)
                    edges.append([input_symbol_index, w])
                    break
                if w < end_hidden_vertex:
                    waves.append([input_symbol_index, w])
                    vertices[w] = tick
        else:
            # continue wave
            new_wave = []
            for wave_index in range(0, len(waves)):
                if found_path:
                    break
                # wave = waves[wave_index]
                current_position = waves[wave_index][-1]
                # first follow the edges
                filtered_edges = filter(lambda x: (x[0] == current_position), edges)

                # if result already done
                if [current_position, output_symbol_index] in filtered_edges:
                    found_path = True
                    print("founded for ", sample[0], "tick ", tick)
                    break

                for f_e in filtered_edges:
                    tmp_w = waves[wave_index].copy()
                    tmp_w.append(f_e[1])
                    new_wave.append(tmp_w)

                rand_branches = [randrange(current_position, vertices_number) for i in range(branches_number)]
                for w in rand_branches:

                    # reach the end
                    if w == output_symbol_index:
                        found_path = True
                        print("founded for ", sample[0], "tick ", tick)
                        waves[wave_index].append(w)
                        # edges.append([[current_position, w]])
                        # add edges
                        prev = waves[wave_index][0]
                        for i in range(1, len(waves[wave_index])):
                            if [prev, waves[wave_index][i]] not in edges:
                                edges.append([prev, waves[wave_index][i]])
                                prev = waves[wave_index][i]

                        break
                    if w < end_hidden_vertex and [current_position, output_symbol_index] not in filtered_edges and vertices[w] < tick - relax_time:
                        tmp_w = waves[wave_index].copy()
                        tmp_w.append(w)
                        new_wave.append(tmp_w)

            # waves
            waves = list(new_wave)


print('edges', edges)

'''
i = 0
for item in waves:
    if i != item[0]:
        print("")
        i = item[0]
    print(item, end=' ')
'''
