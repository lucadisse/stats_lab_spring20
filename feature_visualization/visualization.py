import matplotlib.pyplot as plt

class FeaturePlot:

    def __init__(self, extracted_features, feature_generator, signal_treat=['glu', 'eth', 'sal', 'nea']):
        self.data = extracted_features
        self.feature_generator = feature_generator
        self.chunk_duration = self.feature_generator.chunk_duration
        self.treatments = signal_treat
        self.mouse_ids = list(self.feature_generator.mouse_ids)
        self.indexIdentifier()

    def plotFeatures(self, signal_treat=['glu', 'eth', 'sal', 'nea']):
        #data = self.extracted_features
        #generator = self.feature_generator

        #print(self.list_indexes_mouse_treatment,'\n')
        self.subjectLineplot()
        #plt.show()

    def indexIdentifier(self):
        mouse_ids = self.mouse_ids
        indices = self.data.index
        list_indexes_mouse_treatment = []
        for j in mouse_ids:
            i = 0
            matched_indexes_mouse = [row_id for row_id in indices if str(j) in row_id]
            for treat in self.treatments:
                matched_indexes_mouse_treatment = [row_id for row_id in matched_indexes_mouse if str(j) + '_' + treat in row_id]
                list_indexes_mouse_treatment.append(matched_indexes_mouse_treatment)
        self.list_indexes_mouse_treatment = list_indexes_mouse_treatment

    def subjectLineplot(self):
        feature_number = len(self.data.columns)
        mouse_ids = self.mouse_ids
        chunk_duration = self.chunk_duration
        for f in range(feature_number):
            fig = plt.figure(num=f + 1, figsize=(12, 12))
            i, j = 0, 4
            for mouse in mouse_ids:
                ax = fig.add_subplot(2, 2, mouse_ids.index(mouse)+1)
                for values in self.list_indexes_mouse_treatment[i:j]:
                #for values in [[value] for value in self.list_indexes_mouse_treatment if mouse in value[0]]:
                    ax.plot(list(range(len(values))), self.data.loc[values, self.data.columns[f]], label=values[1][-3:])
                plt.xlabel("Data chunk (" + str(chunk_duration) + ' Min.)')
                plt.ylabel("Feature value")
                plt.title('Mouse ' + str(mouse))
                i, j = i + 4, j + 4
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
            fig.suptitle(str(self.data.columns[f]), fontsize=16, horizontalalignment='center',
                         verticalalignment='top')
            fig.tight_layout(pad=3.0)

        plt.show()



'''    def overallLineplot(self):
        for ff in range(feature_number):
            fig = plt.figure(num=ff + 1, figsize=(12, 12))
            axe = fig.add_subplot(2, 2, 3)
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] * len(mouse_ids)
            axe.plot(list(range(len(list_indexes[0]))), mouse.iloc[list_indexes[0], ff],
                     list(range(len(list_indexes[1]))),
                     mouse.iloc[list_indexes[1], ff], list(range(len(list_indexes[2]))),
                     mouse.iloc[list_indexes[2], ff],
                     list(range(len(list_indexes[3]))), mouse.iloc[list_indexes[3], ff], color='red')
            for i, j in enumerate(axe.lines):
                j.set_color(colors[i])
            plt.title('Mice ' + str(mouse_ids))
            plt.xlabel("Data chunk (" + str(chunk_duration) + ' Min.)')
            plt.ylabel("Feature value")
            plt.legend(treatments, loc='upper right')  # [a,b,c,d],treatments , loc='upper right
            '''

'''previous indexIdentifiers
            #             length = len(indices)
        #             matched_indexes_mouse = []
        # while i < length:
        #matched_indexes_mouse_treatment = []
            #     row_id = indices[i]
            #     if str(j) in row_id:
            #         matched_indexes_mouse.append(row_id)
            #     i += 1

            #mouse = feature_data.iloc[matched_indexes, :]
            #indices = mouse.index
            #length = len(indices)
        #         length = len(matched_indexes_mouse)
        #         list_indexes_mouse_treatment = []
        #         for treat in self.treatments:
        #             i = 0
        #             matched_indexes_mouse_treatment = []
        #             while i < length:
        #                 row_id = matched_indexes_mouse[i]
        #                 if str(j) + '_' + treat in row_id:
        #                     matched_indexes_mouse_treatment.append(row_id)
        #                 i += 1
        #             list_indexes_mouse_treatment.append(matched_indexes_mouse_treatment)
        # self.list_iexes_mouse_treatment = list_indexes_mouse_treatment.append(list_indexes_mouse_treatment)'''


'''    def plotFeatures(self, extracted_features, signal_treat = ['glu', 'eth', 'sal', 'nea']):
        #feature_data = featureDataPreparation(mouse, signal_type, brain_half, mouse_ids, treatments)
        self.treatments = signal_treat
        self.extracted_features = extracted_features
        feature_list, feature_data, mouse_ids, treatments, chunk_duration = feature_data
        print(feature_data)
        feature_number = len(feature_data.columns)
        subplot_position = 1
        for j in mouse_ids:
            i = 0
            indices = feature_data.index
            length = len(indices)
            matched_indexes = []
            while i < length:
                if str(j) in indices[i]:
                    matched_indexes.append(i)
                i += 1

            mouse = feature_data.iloc[matched_indexes,:]
            indices = mouse.index
            length = len(indices)
            list_indexes = []
            for k in range(len(treatments)):
                i = 0
                matched_indexes = []
                while i < length:
                    if str(j)+'.'+str(k+1) in indices[i]:
                        matched_indexes.append(i)
                    i += 1
                list_indexes.append(matched_indexes)
                for f in range(feature_number):
                        fig = plt.figure(num = f+1, figsize=(12,12))
                        ax = fig.add_subplot(2, 2,subplot_position)
                        ax.plot(list(range(len(matched_indexes))), mouse.iloc[matched_indexes,f], label = str(treatments[k]))
                        plt.title('Mouse '+str(j))
                        plt.xlabel("Data chunk ("+str(chunk_duration)+' Min.)')
                        plt.ylabel("Feature value")
                        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
                        fig.suptitle(str(feature_data.columns[f]), fontsize=16, horizontalalignment='center', verticalalignment='top')
                        fig.tight_layout(pad=3.0)
            subplot_position += 1
            for ff in range(feature_number):
                fig = plt.figure(num=ff + 1, figsize=(12,12))
                axe = fig.add_subplot(2, 2, 3)
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']*len(mouse_ids)
                axe.plot(list(range(len(list_indexes[0]))), mouse.iloc[list_indexes[0],ff], list(range(len(list_indexes[1]))),
                         mouse.iloc[list_indexes[1],ff], list(range(len(list_indexes[2]))), mouse.iloc[list_indexes[2],ff],
                         list(range(len(list_indexes[3]))), mouse.iloc[list_indexes[3],ff], color = 'red')
                for i, j in enumerate(axe.lines):
                    j.set_color(colors[i])
                plt.title('Mice ' + str(mouse_ids))
                plt.xlabel("Data chunk ("+str(chunk_duration)+' Min.)')
                plt.ylabel("Feature value")
                plt.legend(treatments , loc='upper right') #[a,b,c,d],treatments , loc='upper right'
        plt.show()'''