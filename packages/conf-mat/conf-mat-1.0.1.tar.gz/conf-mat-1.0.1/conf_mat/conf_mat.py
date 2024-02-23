# Sophisticate Open Confusion Matrix
from tabulate import tabulate  # To Draw The Tables
from termcolor import colored  # To Colored The Data
from numpy import int8, int16, int32, int64  # To Check Data Types
# To Visualize The Data
from matplotlib.pyplot import imshow, tick_params, axhline, axvline, text, \
    colorbar, xticks, yticks, title, xlabel, ylabel, close, savefig, subplots
from webbrowser import open as wb  # To Open The HTML Page


def confusion_matrix(y_or_predicted_y: list, predicted_y_or_y: list) -> list:
    """Confusion Matrix Function"""
    # Checking If The Len > 0
    if len(y_or_predicted_y) > 0:
        # Preparing The Values Counting List
        values = []
        # Concat The Two Lists
        y_and_predicted_y = y_or_predicted_y + predicted_y_or_y
        # Append New Values Into List
        for i in range(len(y_and_predicted_y)):
            if y_and_predicted_y[i] not in values:
                values.append(y_and_predicted_y[i])
        # Sorting The List
        values = sorted(values)
        # Preparing The Confusion Matrix
        confMat = [[0 for _ in values] for _ in values]
        # Counting
        for i in range(len(y_or_predicted_y)):
            confMat[values.index(y_or_predicted_y[i])
                    ][values.index(predicted_y_or_y[i])] += 1
        # Return Confusion Matrix And Values
        return confMat, values
    else:
        # Return Empty Confusion Matrix And None Values
        return [], None


def imshow_config(cm: list, val: list = [], html: bool = False, col: list = []) -> None:
    """Imshow Function"""
    if not html:
        # Preparing Imshow
        imshow(cm, interpolation='nearest', cmap="Paired")  # Or Accent
        # Puting The XLabel
        title(
            "Predicted Classes" if len(cm) > 1 else "Predicted Class", fontsize=10, loc="center")
        # Puting The Imshow ColorBar
        colorbar()
        # Changing The X Axis And Y Axis Places
        tick_params(axis='x', which='both', bottom=False,
                    top=False, labeltop=True, labelbottom=False)
        tick_params(axis='y', which='both', left=False,
                    right=False, labelright=False, labelleft=True)
        # Printing The Title And YLabel
        xlabel("\nConfusion Matrix (Unary Classification)" if len(
            cm) == 1 else "\nConfusion Matrix (Binary Classification)" if len(cm) == 2 else "\nConfusion Matrix (Multi Classification)", loc="center")
        ylabel("Actual Classes" if len(cm) >
               1 else "Actual class", loc="center")
        # Deviding Imshow Squares With Black Bold Lines
        if len(cm) > 1:
            for i in range(1, len(val)):
                # Horizontal Line
                axhline(i - 0.5, color='black',
                        linewidth=2)
                # Vertical Line
                axvline(i - 0.5, color='black',
                        linewidth=2)
    else:
        fig, ax = subplots(figsize=(10, 8))
        conf_mat_disp(col[0], col[1], classes_names=val)
        savefig("conf_mat.png", format="png")
        close()


def label_encoder(y_or_predicted_y: list, isint1: bool, predicted_y_or_y: list, isint2: bool) -> list:
    """Label Encoder Function"""
    # If The First List Not Contain Int Values And The Second List Contain Int Values
    if not isint1 and isint2:
        # Preparing The Values Counting Lists
        target = []
        mining = []
        # Append New Values Into Lists
        for value in y_or_predicted_y:
            if value not in mining:
                mining.append(value)
        for value in predicted_y_or_y:
            if value not in target:
                target.append(value)
        # Sorting The Two Lists
        target = sorted(target)
        mining = sorted(mining)
        # Fix The Difference Between The Two Lists
        if len(mining) > len(target):
            dif = len(mining) - len(target)
            for i in range(dif):
                target.append(len(target)+i)
        # Label Encoding
        for i in range(len(y_or_predicted_y)):
            y_or_predicted_y[i] = target[mining.index(y_or_predicted_y[i])]
        # Preparing X Axis And Y Axis Real Values List
        final = []
        # Append The Real Values In X Axis And Y Axis List
        for i, j in zip(mining, target):
            final.append(i+"/"+str(j))
        # Return Encoded Data
        return y_or_predicted_y, predicted_y_or_y, final
    # If The First List Contain Int Values And The Second List Not Contain Int Values
    elif isint1 and not isint2:
        # Preparing The Values Counting Lists
        target = []
        mining = []
        # Append New Values Into Lists
        for value in y_or_predicted_y:
            if value not in target:
                target.append(value)
        for value in predicted_y_or_y:
            if value not in mining:
                mining.append(value)
        # Sorting The Two Lists
        target = sorted(target)
        mining = sorted(mining)
        # Fix The Difference Between The Two Lists
        if len(mining) > len(target):
            dif = len(mining) - len(target)
            for i in range(dif):
                target.append(len(target)+i)
        # Label Encoding
        for i in range(len(predicted_y_or_y)):
            predicted_y_or_y[i] = target[mining.index(predicted_y_or_y[i])]
        # Preparing X Axis And Y Axis Real Values List
        final = []
        # Append The Real Values In X Axis And Y Axis List
        for i, j in zip(target, mining):
            final.append(str(i)+"/"+j)
        # Return Encoded Data
        return y_or_predicted_y, predicted_y_or_y, final
    # If The Two Lists Not Contain Int Values
    else:
        # Preparing The Values Counting List
        counter = []
        # Concat The Two Lists
        y_and_predicted_y = y_or_predicted_y + predicted_y_or_y
        # Changing The Types Of Values To Str If Not
        y_and_predicted_y = list(map(str, y_and_predicted_y))
        # Append New Values Into List
        for value in y_and_predicted_y:
            if value not in counter:
                counter.append(value)
        # Sorting The List
        counter = sorted(counter)
        # Encode The First List
        for i in range(len(y_or_predicted_y)):
            y_or_predicted_y[i] = counter.index(str(y_or_predicted_y[i]))
        # Encode The Second List
        for i in range(len(predicted_y_or_y)):
            predicted_y_or_y[i] = counter.index(str(predicted_y_or_y[i]))
        # Return Encoded Data
        return y_or_predicted_y, predicted_y_or_y, counter


def check_type(predicted_y_or_y: list) -> bool:
    """Check Type Function"""
    # Preparing Valid Types List
    types_list = [int, int8, int16, int32, int64]
    for value in predicted_y_or_y:
        # Checking If Each Value Is Not Valid
        if type(value) not in types_list:
            return False
        # Checking If Each Value Is Valid
        else:
            continue
    return True


def normalize(cm: list) -> list:
    """Normalize Function"""
    # Copying The Values Into A New List
    rcm = [[cm[i][j] for j in range(len(cm[i]))] for i in range(len(cm))]
    for lines in range(len(rcm)-1):
        for columns in range(len(rcm[lines])):
            # Reverse The Two Diagonal
            help = rcm[lines][columns]
            rcm[lines][columns] = rcm[1 - lines][1-columns]
            rcm[1-lines][1-columns] = help
    return rcm


def classification_report_calculation(cm: list, val: list = [], html: bool = False) -> float | list:
    """Classification Report Calculation"""
    if len(cm) == 2:
        # Calculating The Accuracy Rate
        accuracy = (cm[1][1] + cm[0][0]) / \
            (cm[1][1] + cm[0][0] + cm[1][0] + cm[0][1])
        # Calculating The Error Rate
        error = round(1-accuracy, 2)
        # Percesion Calculation
        try:
            precision = cm[1][1] / (cm[1][1] + cm[0][1])
        except ZeroDivisionError as e1:
            precision = float(1)
        try:
            negative_precision = cm[0][0]/(cm[1][0]+cm[0][0])
        except ZeroDivisionError as e2:
            negative_precision = float(1)
        # Recall Calculation
        try:
            recall = cm[1][1] / (cm[1][1] + cm[1][0])
        except ZeroDivisionError as e3:
            recall = float(1)
        try:
            specificity = cm[0][0]/(cm[0][0]+cm[0][1])
        except ZeroDivisionError as e4:
            specificity = float(1)
        # Support Calculation
        support_1 = cm[1][0] + cm[1][1]
        support_0 = cm[0][1] + cm[0][0]
        # F1-Score Calculation
        try:
            f_score_1 = (2 * precision * recall) / (precision + recall)
        except ZeroDivisionError as e5:
            f_score_1 = float(0)
        try:
            f_score_0 = (2 * negative_precision * specificity) / \
                (negative_precision + specificity)
        except ZeroDivisionError as e6:
            f_score_0 = float(0)
        return accuracy, error, precision, negative_precision, recall, specificity, support_1, support_0, f_score_1, f_score_0
    elif len(cm) > 2:
        # All Values Sum (Correct And Wrong)
        total = 0
        # Preparing The Classification Report Matrix.
        class_repo = [[0 for _ in range(4)] for _ in range(len(val))]
        # Percesion Sum
        per_sum = 0
        # Recall Sum
        rec_sum = 0
        # F1-Score Sum
        f1_sum = 0
        # Weighted Avg
        wa_per_sum = 0
        wa_rec_sum = 0
        wa_f1_sum = 0
        # Preparing The Classification Report Matrix Content
        for i in range(len(class_repo)):
            # Column Sum
            col_sum = 0
            for j in range(len(cm)):
                # Increase In The Column Sum
                col_sum += cm[j][i]
                # Increase In The Total Sum
                total += cm[j][i]
            # Precision Calculation
            try:
                class_repo[i][0] = cm[i][i]/col_sum
                # Increase In The Percesion Sum
                per_sum += class_repo[i][0]
            except ZeroDivisionError as e7:
                class_repo[i][0] = float(1)
                # Increase In The Percesion Sum
                per_sum += class_repo[i][0]
            # Recall Calculation
            try:
                class_repo[i][1] = cm[i][i]/sum(cm[i])
                # Increase In The Recall Sum
                rec_sum += class_repo[i][1]
            except ZeroDivisionError as e8:
                class_repo[i][1] = float(1)
                # Increase In The Recall Sum
                rec_sum += class_repo[i][1]
            # F1-Score Calculation
            try:
                class_repo[i][2] = (
                    (2*class_repo[i][0]*class_repo[i][1])/(class_repo[i][0]+class_repo[i][1]))
                # Increase In The F1-Score Sum
                f1_sum += class_repo[i][2]
            except ZeroDivisionError as e9:
                class_repo[i][2] = float(0)
                # Increase In The F1-Score Sum
                f1_sum += class_repo[i][2]
            # Support Calculation
            class_repo[i][3] = sum(cm[i])
            # Calculating Percesion For The Weighted Avg
            wa_per_sum += class_repo[i][0] * class_repo[i][3]
            # Calculating Recall For The Weighted Avg
            wa_rec_sum += class_repo[i][1] * class_repo[i][3]
            # Calculating F1-Score For The Weighted Avg
            wa_f1_sum += class_repo[i][2] * class_repo[i][3]
            # Round The Precision Value
            class_repo[i][0] = round(class_repo[i][0], 2)
            # Round The Precision Value
            class_repo[i][1] = round(class_repo[i][1], 2)
            # Round The F1-Score Value
            class_repo[i][2] = round(class_repo[i][2], 2)
        # Preparing The Macro Avg And Weighted Avg Matrix.
        class_repo_con = [["Macro Avg", round(per_sum/len(val), 2), round(rec_sum/len(val), 2), round(f1_sum/len(val), 2), total], ["Weighted Avg",
                                                                                                                                    round(wa_per_sum/total, 2), round(wa_rec_sum/total, 2), round(wa_f1_sum/total, 2), total]]
        # Correct Values Sum
        correct = 0
        # Wrong Values Sum
        wrong = 0
        # Colored The Values
        for i in range(len(cm)):
            for j in range(len(cm[i])):
                if i == j:
                    if cm[i][j] != 0:
                        # Increase In The Correct Values Sum
                        correct += cm[i][j]
                        # Colored The Correct Values (Not None)
                        if not html:
                            cm[i][j] = colored(
                                cm[i][j], "yellow", attrs=["bold"])
                    else:
                        # Colored The Correct Values (None)
                        if not html:
                            cm[i][j] = colored(
                                cm[i][j], "green", attrs=["bold"])
                else:
                    if cm[i][j] != 0:
                        # Increase In The Wrong Values Sum
                        wrong += cm[i][j]
                        # Colored The Wrong Values (Not None)
                        if not html:
                            cm[i][j] = colored(cm[i][j], "red", attrs=["bold"])
                    else:
                        # Colored The Wrong Values (None)
                        if not html:
                            cm[i][j] = colored(
                                cm[i][j], "blue", attrs=["bold"])
        # Calculating The Accuracy Rate
        accuracy = correct / total
        # Calculating The Error Rate
        error = wrong / total
        # Insert The Column Of Classes
        val.insert(0, "Classes")
        # Insert Classes In Confusion Matrix
        for i in range(len(cm)):
            cm[i].insert(0, val[i+1])
        # Insert Classes In Classification Report Matrix
        for i in range(len(class_repo)):
            class_repo[i].insert(0, val[i+1])
        return accuracy, error, class_repo, class_repo_con
    else:
        # Printing Error Msg
        print("This Function Work Just With Confusion Matrix of Length >= 2")


def conf_mat_disp(y_or_predicted_y: list, predicted_y_or_y: list, classes_names: list = []) -> None:
    """Confusion Matrix Graphic Display Function"""
    # check The Len Of Two Lists
    if len(y_or_predicted_y) == len(predicted_y_or_y):
        # Changing The Type Of Column Into A List
        y_or_predicted_y = list(y_or_predicted_y)
        predicted_y_or_y = list(predicted_y_or_y)
        # Check The Type For All Data Inside The List
        y_t = check_type(y_or_predicted_y)
        y_p = check_type(predicted_y_or_y)
        if not y_t or not y_p:
            # Label Encoding For Non int Data
            y_or_predicted_y, predicted_y_or_y, valu = label_encoder(
                y_or_predicted_y, y_t, predicted_y_or_y, y_p)
            # Confusion Matrix Calculation
            cm, val = confusion_matrix(y_or_predicted_y, predicted_y_or_y)
            # Check The Type Of Classes Names variable
            if type(classes_names) == list:
                if len(classes_names) == 0:
                    # Keeping The Default List
                    val = valu
                elif len(classes_names) != 0 and (len(classes_names) > len(val) or len(classes_names) < len(val)):
                    # Keeping The Default List
                    val = valu
                    # Printing Error Msg
                    print(
                        "conf_mat_disp : The Number Of Classes Names Is Different From The Number Of Classes")
                else:
                    # Update To The New List
                    val = classes_names
            else:
                # Printing Error Msg
                print("conf_mat_disp : Classes Names Must Be Entered Via A List")
        else:
            # Confusion Matrix Calculation
            cm, val = confusion_matrix(y_or_predicted_y, predicted_y_or_y)
            # Check The Type Of Classes Names variable
            if type(classes_names) == list:
                if len(classes_names) == 0:
                    # Keeping The Default List
                    pass
                elif len(classes_names) != 0 and (len(classes_names) > len(val) or len(classes_names) < len(val)):
                    # Keeping The Default List
                    pass
                    # Printing Error Msg
                    print(
                        "conf_mat_disp : The Number Of Classes Names Is Different From The Number Of Classes")
                else:
                    # Update To The New List
                    val = classes_names
            else:
                # Printing Error Msg
                print("conf_mat_disp : Classes Names Must Be Entered Via A List")
        if len(cm) == 0:
            # Printing Msg
            print("There Is Nothing To See Here :)\n")
        elif len(cm) == 1:
            # Preparing Imshow
            imshow_config(cm)
            # Printing The Real Values In X Axis And Y Axis
            xticks(ticks=[0], labels=[
                f"Positive If Pos OR Negative If Neg ({val[0]})"])
            yticks(ticks=[0], labels=[
                f"Pos OR Neg ({val[0]})"], rotation=90)
            # Preparing The Data Of Square
            annot = [
                f"True Positive OR True Negative \n\nTP OR TN : \n\n{cm[0][0]}"]
            # Printing The Data Into Square
            text(0, 0, f'{annot[0]}', horizontalalignment='center',
                 verticalalignment='center', fontsize=10, color='black')
        elif len(cm) == 2:
            # Reverse The Confusion Matrix
            rcm = normalize(cm)
            # Preparing Imshow
            imshow_config(rcm, val)
            # Printing The Real Values In X Axis And Y Axis
            xticks(ticks=[0, 1], labels=[
                f"Positive ({val[1]})", f"Negative ({val[0]})"])
            yticks(ticks=[0, 1], labels=[
                f"Pos ({val[1]})", f"Neg ({val[0]})"], rotation=0)
            # Preparing The Data Of Each Square
            annot = [[f"True Positive (TP) :\n\n{cm[1][1]}", f"Type II Error (Missed)\n\nFalse Negative (FN) :\n\n{cm[1][0]}"], [
                f"Type I Error (Wrong)\n\nFalse Positive (FP) :\n\n{cm[0][1]}", f"True Negative (TN) :\n\n{cm[0][0]}"]]
            # Printing The Data Into Each Square Of Imshow
            for i in range(len(val)):
                for j in range(len(val)):
                    text(j, i, f'{annot[i][j]}', horizontalalignment='center',
                         verticalalignment='center', fontsize=10, color='black')
        else:
            # Preparing Imshow
            imshow_config(cm, val)
            # Printing The Real Values In X Axis And Y Axis
            xticks(ticks=[*range(len(val))], labels=val)
            yticks(ticks=[*range(len(val))], labels=val, rotation=0)
            # Printing The Data Into Each Square Of Imshow
            for i in range(len(val)):
                for j in range(len(val)):
                    text(j, i, f'{cm[i][j]}', horizontalalignment='center',
                         verticalalignment='center', fontsize=10, color='black')
    else:
        # Printing Error Msg
        print(
            "The List Of Original Values And The List Of Predicted Values Are Not Of The Same Length :(\n")


def conf_mat(y_or_predicted_y: list, predicted_y_or_y: list, classes_names: list = []) -> None:
    """Confusion Matrix Display Function"""
    # check The Len Of Two Lists
    if len(y_or_predicted_y) == len(predicted_y_or_y):
        # Changing The Type Of Column Into A List
        y_or_predicted_y = list(y_or_predicted_y)
        predicted_y_or_y = list(predicted_y_or_y)
        # Check The Type For All Data Inside The List
        y_t = check_type(y_or_predicted_y)
        y_p = check_type(predicted_y_or_y)
        if not y_t or not y_p:
            # Label Encoding For Non int Data
            y_or_predicted_y, predicted_y_or_y, valu = label_encoder(
                y_or_predicted_y, y_t, predicted_y_or_y, y_p)
            # Confusion Matrix Calculation
            cm, val = confusion_matrix(y_or_predicted_y, predicted_y_or_y)
            # Check The Type Of Classes Names variable
            if type(classes_names) == list:
                if len(classes_names) == 0:
                    # Keeping The Default List
                    val = valu
                elif len(classes_names) != 0 and (len(classes_names) > len(val) or len(classes_names) < len(val)):
                    # Keeping The Default List
                    val = valu
                    # Printing Error Msg
                    print(
                        "conf_mat : The Number Of Classes Names Is Different From The Number Of Classes")
                else:
                    # Update To The New List
                    val = classes_names
            else:
                # Printing Error Msg
                print("conf_mat : Classes Names Must Be Entered Via A List")
        else:
            # Confusion Matrix Calculation
            cm, val = confusion_matrix(y_or_predicted_y, predicted_y_or_y)
            # Check The Type Of Classes Names variable
            if type(classes_names) == list:
                if len(classes_names) == 0:
                    # Keeping The Default List
                    pass
                elif len(classes_names) != 0 and (len(classes_names) > len(val) or len(classes_names) < len(val)):
                    # Keeping The Default List
                    pass
                    # Printing Error Msg
                    print(
                        "conf_mat : The Number Of Classes Names Is Different From The Number Of Classes")
                else:
                    # Update To The New List
                    val = classes_names
            else:
                # Printing Error Msg
                print("conf_mat : Classes Names Must Be Entered Via A List")
        if len(cm) == 0:
            # Printing All Data
            print([])
        if len(cm) == 1:
            # Preparing Confusion Matrix
            data1 = [
                [
                    "",
                    f"Positive If Positive OR Negative If Negative ({val[0]})",
                ],
                [
                    f"Positive OR Negative ({val[0]})",
                    f"True Positive OR True Negative \n\n           TP OR TN : \n\n              {cm[0][0]}",
                ],
            ]
            # Preparing The Rate/Score Table
            data2 = [
                [
                    "",
                    "Rate (Score)",
                ],
                [
                    "Accuracy",
                    "1",
                ],
                [
                    "Error",
                    "0",
                ],
            ]
            # Preparing Classification Report
            data3 = [
                [
                    "Precision (P)",
                    "Recall (R)",
                    "F1-Score (F)",
                    "Support (S)",
                ],
                [
                    f"Positive OR Negative ({val[0]})",
                    "1",
                    "1",
                    "1",
                    f"{cm[0][0]}",
                ],
                [
                    "Macro Avg",
                    "1",
                    "1",
                    "1",
                    f"{cm[0][0]}",
                ],
                [
                    "Weighted Avg",
                    "1",
                    "1",
                    "1",
                    f"{cm[0][0]}",
                ],
            ]
            # Printing All Data
            print("\nConfusion Matrix : \n" + "_" *
                  len("Confusion Matrix") + "\n")
            print(tabulate(data1, headers="firstrow", tablefmt="fancy_grid") + "\n")
            print(tabulate(data2, headers="firstrow", tablefmt="fancy_grid") + "\n")
            print("\nClassification Report : \n" + "_" *
                  len("Classification Report") + "\n")
            print(tabulate(data3, headers="firstrow", tablefmt="fancy_grid"))
        elif len(cm) == 2:
            accuracy, error, precision, negative_precision, recall, specificity, support_1, support_0, f_score_1, f_score_0 = classification_report_calculation(
                cm)
            # Preparing Confusion Matrix
            data1 = [
                [
                    "Classes",
                    "Predicted Positive (PP)",
                    "Predicted Negative (PN)",
                    "",
                ],
                [
                    "Actual Positive (P)",
                    "True Positive (" + colored("TP", "yellow",
                                                attrs=['bold']) + f") : {cm[1][1]}",
                    "False Negative (" + colored("FN", "blue",
                                                 attrs=['bold']) + f") : {cm[1][0]}\nType II Error (Missed)",
                ],
                [
                    "Actual Negative (N)",
                    "False Positive (" + colored("FP", "red",
                                                 attrs=['bold']) + f") : {cm[0][1]}\nType I Error (Wrong)",
                    "True Negative (" + colored("TN", "green",
                                                attrs=['bold']) + f") : {cm[0][0]}",
                ],
            ]
            # Preparing The Rate/Score Table
            data2 = [
                [
                    "",
                    "Rate (Score)",
                ],
                [
                    "Accuracy",
                    "Correct        " + colored("TP", "yellow", attrs=['bold']) + " + " + colored("TN", "green", attrs=['bold']) + "\n" + "_" * len("Correct") + " : " + "_" *
                    len("TP + FP + FN + TN") + "  OR  1 - Error " + " =  " +
                    f"{round(accuracy, 2)}" +
                    "\n\n Total    " + colored("TP", "yellow", attrs=['bold']) + " + " + colored("FP", "red", attrs=[
                        'bold']) + " + " + colored("FN", "blue", attrs=['bold']) + " + " + colored("TN", "green", attrs=['bold']),
                ],
                [
                    "Error",
                    "Wrong        " + colored("FP", "red", attrs=['bold']) + " + " + colored("FN", "blue", attrs=['bold']) + "\n" + "_" * len("Wrong") + " : " + "_" *
                    len("TP + FP + FN + TN") + "  OR  1 - Accuracy " +
                    " =  " + f"{error}" + "\n\nTotal   " + colored("TP", "yellow", attrs=['bold']) + " + " + colored("FP", "red", attrs=[
                        'bold']) + " + " + colored("FN", "blue", attrs=['bold']) + " + " + colored("TN", "green", attrs=['bold']),
                ],
            ]
            # Preparing Classification Report
            data3 = [
                [
                    "Precision (P)",
                    "Recall (R)",
                    "F1-Score (F)",
                    "Support (S)",
                ],
                [
                    f"Positive ({val[1]})",
                    "P1 (PPV): \n\n  " + colored("TP", "yellow", attrs=['bold']) + "\n" + "_" *
                    len("TP + FP") + "  = " +
                    f"{round(precision, 2)}" + "\n\n" + colored("TP", "yellow",
                                                                attrs=['bold']) + " + " + colored("FP", "red", attrs=['bold']),
                    f"R1 (Sensitivity):\n\n  " + colored("TP", "yellow", attrs=['bold']) + "\n" + "_" * len("TP + FN") +
                    "  = " + f"{round(recall, 2)}" + "\n\n" + colored("TP", "yellow", attrs=[
                        'bold']) + " + " + colored("FN", "blue", attrs=['bold']),
                    "F1 : \n\n" + "2 x P1 x R1\n" + "_" * len("2 x P1 x R1") +
                    "  = " + f"{round(f_score_1, 2)}" + "\n\n  P1 + R1",
                    "S1 : \n\n\n " + colored("TP", "yellow", attrs=['bold']) + " + " + colored(
                        "FN", "blue", attrs=['bold']) + f" = {support_1}",
                ],
                [
                    f"Negative ({val[0]})",
                    f"P0 (NPV): \n\n  " + colored("TN", "green", attrs=['bold']) + "\n" + "_" *
                    len("TN + FN") + "  = " +
                    f"{round(negative_precision, 2)}" +
                    "\n\n" +
                    colored("TN", "green", attrs=[
                            'bold']) + " + " + colored("FN", "blue", attrs=['bold']),
                    f"R0 (Specificity): \n\n  " + colored("TN", "green", attrs=['bold']) + "\n" + "_" * len("TN + FP") +
                    "  = " + f"{round(specificity, 2)}" +
                    "\n\n" + colored("TN", "green",
                                     attrs=['bold']) + " + " + colored("FP", "red", attrs=['bold']),
                    "F0 : \n\n" + "2 x P0 x R0\n" + "_" * len("2 x P0 x R0") +
                    "  = " + f"{round(f_score_0, 2)}" + "\n\n  P0 + R0",
                    "S0 : \n\n\n " + colored("FP", "red", attrs=['bold']) + " + " + colored(
                        "TN", "green", attrs=['bold']) + f" = {support_0}",
                ],
                [
                    "Macro Avg",
                    "P1 + P0\n" + "_" *
                    len("P1 + P0") + "  = " +
                    f"{round((precision + negative_precision)/2, 2)}" +
                    "\n\n   2",
                    "R1 + R0\n" + "_" *
                    len("R1 + R0") + "  = " +
                    f"{round((recall + specificity)/2, 2)}" + "\n\n   2",
                    "F1 + F0\n" + "_" * len("F1 + F0") + "  = " +
                    f"{round((f_score_1 + f_score_0)/2, 2)}" + "\n\n   2",
                    f"TS = {support_0 + support_1}",
                ],
                [
                    "Weighted Avg",
                    "W1\n" + "_" * len("TS") + "  = " +
                    f"{round(((precision * support_1) + (negative_precision * support_0))/(support_0 + support_1), 2)}" + "\n\nTS",
                    "W2\n" + "_" * len("TS") + "  = " +
                    f"{round(((recall * support_1) + (specificity * support_0))/(support_0 + support_1), 2)}" + "\n\nTS",
                    "W3\n" + "_" * len("TS") + "  = " +
                    f"{round(((f_score_1 * support_1) + (f_score_0 * support_0))/(support_1 + support_0),2)}" + "\n\nTS",
                    f"TS = {support_0 + support_1}",
                ],
            ]
            # Printing All Data
            print("\nConfusion Matrix : \n" + "_" *
                  len("Confusion Matrix") + "\n")
            print(tabulate(data1, headers="firstrow", tablefmt="fancy_grid") + "\n")
            print(tabulate(data2, headers="firstrow", tablefmt="fancy_grid") + "\n")
            print("\nClassification Report : \n" + "_" *
                  len("Classification Report") + "\n")
            print(tabulate(data3, headers="firstrow", tablefmt="fancy_grid"))
            print("\nPPV : Positive Predictive Value")
            print("\nNPV : Negative Predictive Value")
            print("\nW1 = (P1 x S1) + (P0 x S0)")
            print("\nW2 = (R1 x S1) + (R0 x S0)")
            print("\nW3 = (F1 x S1) + (F0 x S0)")
            print("\nTS : Total Support = S1 + S0")
            print(
                "\nNote : All Real Numbers Are Rounded With Two Digits After The Comma\n")
        else:
            accuracy, error, class_repo, class_repo_con = classification_report_calculation(
                cm, val)
            # Concat The Classes with Confusion Matrix
            data1 = [val] + cm
            # Preparing The Rate/Score Table
            data2 = [
                [
                    "",
                    "Rate (Score)",
                ],
                [
                    "Accuracy",
                    "Correct      " + "Sum Of " + colored("Yellow", "yellow", attrs=['bold']) + " Values\n" + "_" * len("Correct") + " : " + "_" *
                    len("Sum Of Yellow And Red Values") + "  OR  1 - Error " + " =  " +
                    f"{round(accuracy, 2)}" +
                    "\n\n Total    Sum Of " +
                    colored("Yellow", "yellow", attrs=[
                            'bold'])+" And "+colored("Red", "red", attrs=['bold'])+" Values",
                ],
                [
                    "Error",
                    "Wrong        " + "Sum Of " + colored("Red", "red", attrs=['bold']) + " Values\n" + "_" * len("Wrong") + " : " + "_" *
                    len("Sum Of Yellow And Red Values") + "  OR  1 - Accuracy " + " =  " +
                    f"{round(error, 2)}" +
                    "\n\nTotal   Sum Of " +
                    colored("Yellow", "yellow", attrs=[
                            'bold'])+" And "+colored("Red", "red", attrs=['bold'])+" Values",
                ],
            ]
            # Concat The header Row With The Classification Report Matrix
            data3 = [["", "Precision (P)", "Recall (R)",
                     "F1-Score (F)", "Support (S)"]] + class_repo + class_repo_con
            # Printing All Data
            print("\nConfusion Matrix : \n" + "_" *
                  len("Confusion Matrix") + "\n")
            print(tabulate(data1, headers="firstrow", tablefmt="fancy_grid") + "\n")
            print(colored("Yellow", "yellow", attrs=['bold']), end=" ")
            print(" : Not None Correct Values / True Positive (TP) OR True Negative (TN)")
            print(colored("Red", "red", attrs=['bold']), end=" ")
            print(
                "    : Not None Wrong Values / False Positive (FP) OR False Negative (FN)")
            print(colored("Green", "green", attrs=['bold']), end=" ")
            print("  : None Correct Values")
            print(colored("Blue", "blue", attrs=['bold']), end=" ")
            print("   : None Wrong Values\n")
            print(tabulate(data2, headers="firstrow", tablefmt="fancy_grid") + "\n")
            print("\nClassification Report : \n" + "_" *
                  len("Classification Report") + "\n")
            print(tabulate(data3, headers="firstrow", tablefmt="fancy_grid") + "\n")
            print("Precision    : " + colored("Yellow", "yellow", attrs=[
                  'bold']) + " Value / Sum Of " + colored("Yellow", "yellow", attrs=['bold']) + " Value Column\n")
            print("Recall       : " + colored("Yellow", "yellow", attrs=[
                  'bold']) + " Value / Sum Of " + colored("Yellow", "yellow", attrs=['bold']) + " Value Row\n")
            print("F1-Score     : (2 x Precision x Recall) / (Precision + Recall)\n")
            print("Support      : Sum Of Each Row\n")
            print("Macro Avg    :\n")
            print(
                "               Precision : (Sum Of Precision Column) / Classes Count\n")
            print("               Recall    : (Sum Of Recall Column) / Classes Count\n")
            print("               F1-Score  : (Sum Of F1-Score Column) / Classes Count\n")
            print("               Support   : Total (Sum Of All Matrix)\n")
            print("Weighted Avg :\n")
            print(
                "               Precision : (Sum Of (Precision x support)) / Total (Sum Of All Matrix)\n")
            print(
                "               Recall    : (Sum Of (Recall x Support)) / Total (Sum Of All Matrix)\n")
            print(
                "               F1-Score  : (Sum Of (F1-Score x Support)) / Total (Sum Of All Matrix)\n")
            print("               Support   : Total (Sum Of All Matrix)\n")
            print("Note : All Real Numbers Are Rounded With Two Digits After The Comma\n")
    else:
        # Printing Error Msg
        print(
            "The List Of Original Values And The List Of Predicted Values Are Not Of The Same Length :(\n")


def update_html(void: None) -> None:
    """HTML Code Update Function"""
    with open("conf_mat.html", "r") as file:
        # Reading The File Line By Line And Seting Him Into A List
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i] == "<table>\n":
                # Add border=1
                lines[i] = "<table border=1>\n"
    with open("conf_mat.html", "w") as file:
        # Writing New And Missing HTML Code 
        file.write("<!DOCTYPE html>\n")
        file.write('<html lang="en">\n\n')
        file.write("<head>\n")
        file.write('<meta charset="UTF-8">\n')
        file.write(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        file.write("<title>conf_mat</title>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.writelines(lines)
        file.write("</body>\n")
        file.write("</html>")


def conf_mat_to_html(y_or_predicted_y: list, predicted_y_or_y: list, classes_names: list = []) -> None:
    """Confusion Matrix Display/Graphic Display Function (All In One HTML Page)"""
    # check The Len Of Two Lists
    if len(y_or_predicted_y) == len(predicted_y_or_y):
        # Changing The Type Of Column Into A List
        y_or_predicted_y = list(y_or_predicted_y)
        predicted_y_or_y = list(predicted_y_or_y)
        # Check The Type For All Data Inside The List
        y_t = check_type(y_or_predicted_y)
        y_p = check_type(predicted_y_or_y)
        if not y_t or not y_p:
            # Label Encoding For Non int Data
            y_or_predicted_y, predicted_y_or_y, valu = label_encoder(
                y_or_predicted_y, y_t, predicted_y_or_y, y_p)
            # Confusion Matrix Calculation
            cm, val = confusion_matrix(y_or_predicted_y, predicted_y_or_y)
            # Check The Type Of Classes Names variable
            if type(classes_names) == list:
                if len(classes_names) == 0:
                    # Keeping The Default List
                    val = valu
                elif len(classes_names) != 0 and (len(classes_names) > len(val) or len(classes_names) < len(val)):
                    # Keeping The Default List
                    val = valu
                    # Printing Error Msg
                    print(
                        "conf_mat_to_html : The Number Of Classes Names Is Different From The Number Of Classes")
                else:
                    # Update To The New List
                    val = classes_names
            else:
                # Printing Error Msg
                print("conf_mat_to_html : Classes Names Must Be Entered Via A List")
        else:
            # Confusion Matrix Calculation
            cm, val = confusion_matrix(y_or_predicted_y, predicted_y_or_y)
            # Check The Type Of Classes Names variable
            if type(classes_names) == list:
                if len(classes_names) == 0:
                    # Keeping The Default List
                    pass
                elif len(classes_names) != 0 and (len(classes_names) > len(val) or len(classes_names) < len(val)):
                    # Keeping The Default List
                    pass
                    # Printing Error Msg
                    print(
                        "conf_mat_to_html : The Number Of Classes Names Is Different From The Number Of Classes")
                else:
                    # Update To The New List
                    val = classes_names
            else:
                # Printing Error Msg
                print("conf_mat_to_html : Classes Names Must Be Entered Via A List")
        # Creating The Confusion Matrix Heatmap (Png Format) In Working Direcory
        col = [y_or_predicted_y, predicted_y_or_y]
        imshow_config(cm, val, html=True, col=col)
        if len(cm) == 0:
            # Print Msg
            print("No HTML File Generated :(")
        elif len(cm) == 1:
            # Preparing Confusion Matrix
            data1 = [
                [
                    "",
                    f"Positive If Positive OR Negative If Negative ({val[0]})",
                ],
                [
                    f"Positive OR Negative ({val[0]})",
                    f"True Positive OR True Negative \n\n           TP OR TN : \n\n              {cm[0][0]}",
                ],
            ]
            # Preparing The Rate/Score Table
            data2 = [
                [
                    "",
                    "Rate (Score)",
                ],
                [
                    "Accuracy",
                    "1",
                ],
                [
                    "Error",
                    "0",
                ],
            ]
            # Preparing Classification Report
            data3 = [
                [
                    "Precision (P)",
                    "Recall (R)",
                    "F1-Score (F)",
                    "Support (S)",
                ],
                [
                    f"Positive OR Negative ({val[0]})",
                    "1",
                    "1",
                    "1",
                    f"{cm[0][0]}",
                ],
                [
                    "Macro Avg",
                    "1",
                    "1",
                    "1",
                    f"{cm[0][0]}",
                ],
                [
                    "Weighted Avg",
                    "1",
                    "1",
                    "1",
                    f"{cm[0][0]}",
                ],
            ]
            # Writing All Data
            with open("conf_mat.html", "w") as file:
                file.write("Confusion Matrix :\n<br>\n<br>\n")
                file.write(tabulate(data1, headers="firstrow",
                                    tablefmt="html") + "\n<br>\n<br>\n")
                file.write(tabulate(data2, headers="firstrow",
                                    tablefmt="html") + "\n<br>\n<br>\n")
                file.write("Classification Report :\n<br>\n<br>\n")
                file.write(
                    tabulate(data3, headers="firstrow", tablefmt="html") + "\n<br>\n<br>\n")
                file.write("Confusion Matrix Display : \n<br>\n<br>\n")
                file.write('<img src="conf_mat.png" alt="Confusion Matrix">\n')
            # Update HTML Code
            update_html(None)
            # Print The Success Msg
            print("\nHTML File Generated Succesfuly :)\n")
            # Opening HTML Page
            wb("conf_mat.html")
        elif len(cm) == 2:
            accuracy, error, precision, negative_precision, recall, specificity, support_1, support_0, f_score_1, f_score_0 = classification_report_calculation(
                cm)
            # Preparing Confusion Matrix
            data1 = [
                [
                    "Classes",
                    "Predicted Positive (PP)",
                    "Predicted Negative (PN)",
                    "",
                ],
                [
                    "Actual Positive (P)",
                    f"True Positive (TP) : {cm[1][1]}",
                    f"False Negative (FN) / Type II Error (Missed) : {cm[1][0]}",
                ],
                [
                    "Actual Negative (N)",
                    f"False Positive (FP) Type I Error (Wrong) : {cm[0][1]}",
                    f"True Negative (TN) : {cm[0][0]}",
                ],
            ]
            # Preparing The Rate/Score Table
            data2 = [
                [
                    "",
                    "Rate (Score)",
                ],
                [
                    "Accuracy",
                    f"Correct / Total : (TP + TN) / (TP + FP + FN + TN) = {round(accuracy, 2)}",
                ],
                [
                    "Error",
                    f"Wrong / Total : (FP + FN) / (TP + FP + FN + TN) = {error}",
                ],
            ]
            # Preparing Classification Report
            data3 = [
                [
                    "Precision (P)",
                    "Recall (R)",
                    "F1-Score (F)",
                    "Support (S)",
                ],
                [
                    f"Positive ({val[1]})",
                    f"P1 (PPV): TP / (TP + FP) = {round(precision, 2)}",
                    f"R1 (Sensitivity): TP / (TP + FN) = {round(recall, 2)}",
                    f"F1 : (2 x P1 x R1) / (P1 + R1) = {round(f_score_1, 2)}",
                    f"S1 : TP + FN = {support_1}",
                ],
                [
                    f"Negative ({val[0]})",
                    f"P0 (NPV): TN / (TN + FN) = {round(negative_precision, 2)}",
                    f"R0 (Specificity): TN / (TN + FP) = {round(specificity, 2)}",
                    f"F0 : (2 x P0 x R0) /  (P0 + R0) = {round(f_score_0, 2)}",
                    f"S0 : FP + TN = {support_0}",
                ],
                [
                    "Macro Avg",
                    f"(P1 + P0) / 2 = {round((precision + negative_precision)/2, 2)}",
                    f"(R1 + R0) / 2 = {round((recall + specificity)/2, 2)}",
                    f"(F1 + F0) / 2 = {round((f_score_1 + f_score_0)/2, 2)}",
                    f"TS = {support_0 + support_1}",
                ],
                [
                    "Weighted Avg",
                    f"W1 / TS = {round(((precision * support_1) + (negative_precision * support_0))/(support_0 + support_1), 2)}",
                    f"W2 / TS = {round(((recall * support_1) + (specificity * support_0))/(support_0 + support_1), 2)}",
                    f"W3 / TS = {round(((f_score_1 * support_1) + (f_score_0 * support_0))/(support_1 + support_0),2)}",
                    f"TS = {support_0 + support_1}",
                ],
            ]
            # Writing All Data
            with open("conf_mat.html", "w") as file:
                file.write("<u><b>Confusion Matrix</b></u> : \n<br>\n<br>\n")
                file.write(tabulate(data1, headers="firstrow",
                           tablefmt="html") + "\n<br>\n<br>\n")
                file.write(tabulate(data2, headers="firstrow",
                           tablefmt="html") + "\n<br>\n<br>\n")
                file.write(
                    "<u><b>Classification Report</b></u> : \n<br>\n<br>\n")
                file.write(tabulate(data3, headers="firstrow",
                           tablefmt="html") + "\n<br>\n<br>\n")
                file.write(
                    "<u><b>PPV</b></u> : Positive Predictive Value\n<br>\n<br>\n")
                file.write(
                    "<u><b>NPV</b></u> : Negative Predictive Value\n<br>\n<br>\n")
                file.write("<b>W1</b> = (P1 x S1) + (P0 x S0)\n<br>\n<br>\n")
                file.write("<b>W2</b> = (R1 x S1) + (R0 x S0)\n<br>\n<br>\n")
                file.write("<b>W3</b> = (F1 x S1) + (F0 x S0)\n<br>\n<br>\n")
                file.write(
                    "<b>TS</b> : Total Support = S1 + S0\n<br>\n<br>\n<br>\n")
                file.write(
                    "<u><b>Note</b></u> : All Real Numbers Are Rounded With Two Digits After The Comma\n<br>\n<br>\n<br>\n<br>")
                file.write(
                    "<u><b>Confusion Matrix Display</b></u> : \n<br>\n<br>\n")
                file.write('<img src="conf_mat.png" alt="Confusion Matrix">\n')
            # Update HTML Code
            update_html(None)
            # Print The Success Msg
            print("\nHTML File Generated Succesfuly :)\n")
            # Opening HTML Page
            wb("conf_mat.html")
        else:
            accuracy, error, class_repo, class_repo_con = classification_report_calculation(
                cm, val, html=True)
            # Concat The Classes with Confusion Matrix
            data1 = [val] + cm
            # Preparing The Rate/Score Table
            data2 = [
                [
                    "",
                    "Rate (Score)",
                ],
                [
                    "Accuracy",
                    f"Correct / Total : Sum Of Left Diagonal Values / Total (Sum Of All Matrix) OR  1 - Error = {round(accuracy, 2)}",
                ],
                [
                    "Error",
                    f"Wrong / Total : (Total (Sum Of All Matrix) - Sum Of Left Diagonal Values) / Total (Sum Of All Matrix) OR  1 - Accuracy = {round(error, 2)}",
                ],
            ]
            # Concat The header Row With The Classification Report Matrix
            data3 = [["", "Precision (P)", "Recall (R)",
                     "F1-Score (F)", "Support (S)"]] + class_repo + class_repo_con
            # Writing All Data
            with open("conf_mat.html", "w") as file:
                file.write("<u><b>Confusion Matrix</b></u> : \n<br>\n<br>\n")
                file.write(tabulate(data1, headers="firstrow",
                           tablefmt="html") + "\n<br>\n<br>\n")
                file.write(tabulate(data2, headers="firstrow",
                           tablefmt="html") + "\n<br>\n<br>\n")
                file.write(
                    "<u><b>Classification Report<b></u> :\n<br>\n<br>\n")
                file.write(tabulate(data3, headers="firstrow",
                           tablefmt="html") + "\n<br>\n<br>\n")
                file.write(
                    "<b><u>Precision</u></b> " + "&nbsp;" * 3 + ": Sum Of True Prediction For Each Value (Left Diagonal) / Sum Of Value Column\n<br>\n<br>\n")
                file.write(
                    "<u><b>Recall</b></u>    " + "&nbsp;" * 8 + ": Sum Of True Prediction For Each Value (diagonal) / Sum Of Value Row\n<br>\n<br>\n")
                file.write(
                    "<u><b>F1-Score</b></u>  " + "&nbsp;" * 3 + ": (2 x Precision x Recall) / (Precision + Recall)\n<br>\n<br>\n")
                file.write(
                    "<u><b>Support</b></u>   " + "&nbsp;" * 5 + ": Sum Of Each Row\n<br>\n<br>\n")
                file.write("<u><b>Macro Avg</b></u> :\n<br>\n<br>\n")
                file.write(
                    "&nbsp;" * 15 + "Precision : (Sum Of Precision Column) / Classes Count\n<br>\n<br>\n")
                file.write(
                    "&nbsp;" * 15 + "Recall    " + "&nbsp;" * 5 + ": (Sum Of Recall Column) / Classes Count\n<br>\n<br>\n")
                file.write(
                    "&nbsp;" * 15 + "F1-Score  : (Sum Of F1-Score Column) / Classes Count\n<br>\n<br>\n")
                file.write(
                    "&nbsp;" * 15 + "Support   " + "&nbsp;" * 2 + ": Total (Sum Of All Matrix)\n<br>\n<br>\n")
                file.write("<u><b>Weighted Avg</b></u> :\n<br>\n<br>\n")
                file.write(
                    "&nbsp;" * 15 + "Precision : (Sum Of (Precision x support)) / Total (Sum Of All Matrix)\n<br>\n<br>\n")
                file.write(
                    "&nbsp;" * 15 + "Recall    " + "&nbsp;" * 5 + ": (Sum Of (Recall x Support)) / Total (Sum Of All Matrix)\n<br>\n<br>\n")
                file.write(
                    "&nbsp;" * 15 + "F1-Score  : (Sum Of (F1-Score x Support)) / Total (Sum Of All Matrix)\n<br>\n<br>\n")
                file.write(
                    "&nbsp;" * 15 + "Support   " + "&nbsp;" * 2 + ": Total (Sum Of All Matrix)\n<br>\n<br>\n<br>\n")
                file.write(
                    "<u><b>Note</b></u> : All Real Numbers Are Rounded With Two Digits After The Comma\n<br>\n<br>\n<br>\n<br>\n")
                file.write(
                    "<u><b>Confusion Matrix Display</b></u> : \n<br>\n<br>\n")
                file.write('<img src="conf_mat.png" alt="Confusion Matrix">\n')
            # Update HTML Code
            update_html(None)
            # Print The Success Msg
            print("\nHTML File Generated Succesfuly :)\n")
            # Opening HTML Page
            wb("conf_mat.html")
