from flask import request, render_template, flash
from main.core import create_plot
import numpy as np
from flask import flash

from main.kjtscfvariations import KJointSCFManager


def k_joint_route():
    # plot data for brace a
    plot_data_a_cs, plot_data_a_bs = None, None

    # plot data for brace b
    plot_data_b_cs,plot_data_b_bs = None, None

    show_table = False
    kjt_obj = None

    b = None # calculated variable todo

    # chord inputs
    d1 = request.form.get('D', '')
    thk1 = request.form.get('T', '')

    # brace A inputs
    d2_a = request.form.get('dA', '')
    thk2_a = request.form.get('tA', '')
    theta_a = request.form.get('thetaA', '')

    # brace B inputs
    d2_b = request.form.get('dB', '')
    thk2_b = request.form.get('tB', '')
    theta_b = request.form.get('thetaB', '')

    # gap
    g_ab = request.form.get('g_ab', '')

    # chord length and fixity (todo)
    L = request.form.get('L', '')
    C = request.form.get('C', '')
    load_type = request.form.get('load_type', '')  # update var names

    x_axis_desc = request.form.get('x_axis_desc', '')  # todo align var names
    scf_options = request.form.get('scf_options', '')  # "scf_only" or "scf_stress_adjusted"

    if request.method == 'POST':
        # Check if any input is None and flash messages accordingly
        invalid_inputs = [v is None for v in [d1, thk1, d2_a, thk2_a, theta_a, d2_b, thk2_b, theta_b, g_ab, L, C]]

        if any(invalid_inputs):
            flash("Please enter valid numbers for all fields.")

        else:
            try:
                show_table = True  # variable to indicate that SCFs can be presented in a data table
                # convert angles to radians
                theta_a_radians, theta_b_radians = np.radians(float(theta_a)), np.radians(float(theta_b))

                # store all inputs in a dict and convert to floats
                input_fields = {"D": float(d1), "T": float(thk1), "dA": float(d2_a), "tA": float(thk2_a),
                                "thetaA": theta_a_radians, "dB": float(d2_b), "tB": float(thk2_b),
                                "thetaB": theta_b_radians, "g_ab": float(g_ab), "L":float(L), "C": float(C)}


                # calculated values todo example
                b = input_fields["D"] / input_fields["T"]

                stress_adjusted = True if scf_options == "scf_stress_adjusted" else False

                kjt_obj = KJointSCFManager(x_axis_desc, input_fields, stress_adjusted)
                kjt_obj.get_k_joint_scfs(load_type)

                # convert theta angles back to radians for plotting
                kjt_obj.convert_angles_to_degrees(x_axis_desc)

                # brace A plots
                # chord side
                plot_data_a_cs = create_plot(kjt_obj.params, {("axial crown", "red", "-"): kjt_obj.scf_a_axial_chord_crowns,
                                                              ("axial saddle", "orange", "-"): kjt_obj.scf_a_axial_chord_saddles,
                                                              ("IPB crown", "blue", "-"): kjt_obj.scf_ipb_a_chord_crowns,
                                                              ("OPB saddle", "green", "-"): kjt_obj.scf_opb_a_chord_saddles,
                                                              ("axial crown stress_adjusted", "red", "--"): kjt_obj.scf_a_axial_chord_crowns_adj,
                                                              ("axial saddle stress_adjusted", "orange", "--"): kjt_obj.scf_a_axial_chord_saddles_adj,
                                                              ("IPB crown stress_adjusted", "blue", "--"): kjt_obj.scf_ipb_a_chord_crowns_adj,
                                                              ("OPB saddle stress_adjusted", "green", "--"): kjt_obj.scf_opb_a_chord_saddles_adj
                                                              },
                                             x_axis_desc, stress_adjusted=stress_adjusted)  # chordside

                # brace side
                plot_data_a_bs = create_plot(kjt_obj.params, {("axial crown", "red", "-"): kjt_obj.scf_a_axial_brace_crowns,
                                                              ("axial saddle", "orange", "-"): kjt_obj.scf_a_axial_brace_saddles,
                                                              ("IPB crown", "blue", "-"): kjt_obj.scf_ipb_a_brace_crowns,
                                                              ("OPB saddle", "green", "-"): kjt_obj.scf_opb_a_brace_saddles,
                                                              ("axial crown stress_adjusted", "red", "--"): kjt_obj.scf_a_axial_brace_crowns_adj,
                                                              ("axial saddle stress_adjusted", "orange", "--"): kjt_obj.scf_a_axial_brace_saddles_adj,
                                                              ("IPB crown stress_adjusted", "blue", "--"): kjt_obj.scf_ipb_a_brace_crowns_adj,
                                                              ("OPB saddle stress_adjusted", "green", "--"): kjt_obj.scf_opb_a_brace_saddles_adj
                                                              },
                                             x_axis_desc, stress_adjusted=stress_adjusted)  # braceside

                # brace B plots
                # chord side
                plot_data_b_cs = create_plot(kjt_obj.params, {("axial crown", "red", "-"): kjt_obj.scf_b_axial_chord_crowns,
                                                              ("axial saddle", "orange", "-"): kjt_obj.scf_b_axial_chord_saddles,
                                                              ("IPB crown", "blue", "-"): kjt_obj.scf_ipb_b_chord_crowns,
                                                              ("OPB saddle", "green", "-"): kjt_obj.scf_opb_b_chord_saddles,
                                                              ("axial crown stress_adjusted", "red", "--"): kjt_obj.scf_b_axial_chord_crowns_adj,
                                                              ("axial saddle stress_adjusted", "orange", "--"): kjt_obj.scf_b_axial_chord_saddles_adj,
                                                              ("IPB crown stress_adjusted", "blue", "--"): kjt_obj.scf_ipb_b_chord_crowns_adj,
                                                              ("OPB saddle stress_adjusted", "green", "--"): kjt_obj.scf_opb_b_chord_saddles_adj
                                                              },
                                             x_axis_desc, stress_adjusted=stress_adjusted)  # chordside

                # brace side
                plot_data_b_bs = create_plot(kjt_obj.params, {("axial crown", "red", "-"): kjt_obj.scf_b_axial_brace_crowns,
                                                              ("axial saddle", "orange", "-"): kjt_obj.scf_b_axial_brace_saddles,
                                                              ("IPB crown", "blue", "-"): kjt_obj.scf_ipb_b_brace_crowns,
                                                              ("OPB saddle", "green", "-"): kjt_obj.scf_opb_b_brace_saddles,
                                                              ("axial crown stress_adjusted", "red", "--"): kjt_obj.scf_b_axial_brace_crowns_adj,
                                                              ("axial saddle stress_adjusted", "orange", "--"): kjt_obj.scf_b_axial_brace_saddles_adj,
                                                              ("IPB crown stress_adjusted", "blue", "--"): kjt_obj.scf_ipb_b_brace_crowns_adj,
                                                              ("OPB saddle stress_adjusted", "green", "--"): kjt_obj.scf_opb_b_brace_saddles_adj
                                                              },
                                             x_axis_desc, stress_adjusted=stress_adjusted)  # braceside

            except Exception as e:
                flash(f"An error occurred: {e}")

    else:
        pass

    return render_template('k_joint.html',
                           plot_data_a_cs=plot_data_a_cs, plot_data_a_bs=plot_data_a_bs,  # brace A (c-s and b-s)
                           plot_data_b_cs=plot_data_b_cs, plot_data_b_bs=plot_data_b_bs,  # brace B (c-s and b-s)
                           show_table=show_table,
                           D=d1, T=thk1,  # chord
                           dA=d2_a, tA=thk2_a, thetaA=theta_a, # brace A
                           dB=d2_b, tB=thk2_b, thetaB=theta_b,  # brace B
                           g_ab=g_ab,  # gap
                           L=L, C=C,
                           load_type=load_type,
                           x_axis_desc=x_axis_desc,
                           scf_options=scf_options,
                           kjt_obj=kjt_obj,
                           b=b)  # calculated values