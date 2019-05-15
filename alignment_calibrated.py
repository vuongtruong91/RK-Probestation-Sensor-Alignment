#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Alignment Measurement Plotter
#3/21/18

#############################
#							#
#		  Imports			#
#							#
#############################

from __future__ import division
import ROOT as R
import os.path
import sys
from array import array
#import matplotlib.pyplot as plt
#import matplotlib.ticker as mtick

#############################
#							#
#		  Globals			#
#							#
#############################


def my_index(L, obj):
     try:
             return L.index(obj)
     except ValueError:
             return -1

def readvar(L, obj):
     if obj == -1:
             return -1
     else:
             return float(L[obj])


alignDataFiles = sys.argv[1]
#PSS_fid = sys.argv[2]
#PSP_fid = sys.argv[3]

nameForSave = alignDataFiles.replace('.txt','')
print nameForSave
#if PSS_fid == "0":
#	pss_xoff = 420
#	pss_yoff = -185
#else:
#	pss_xoff = 525
#	pss_yoff = -110
#if PSP_fid == "0":
#	psp_xoff = 420
#	psp_yoff = -185
#else:
#	psp_xoff = 525
#	psp_yoff = -110

#print "Offsets", pss_xoff, pss_yoff, psp_xoff, psp_yoff

filX = array('i', [ 0 ])
filY = array('i', [ 0 ])
x = array('f',[ 0. ])
y = array('f',[ 0. ])
pixX = array('f',[ 0. ])
pixY = array('f',[ 0. ])
edge = array('i',[ 0 ])
desig = array('i',[ 0 ])
#fidX = array('f',[ 0. ])
#fidY = array('f',[ 0. ])
#TfidX = array('f',[ 0. ])
#TfidY = array('f',[ 0. ])
#BfidX = array('f',[ 0. ])
#BfidY = array('f',[ 0. ])
fidX = array('f',[ 0. ]) #NOTE: fidX is real world positions, for both fiducials and edges
fidY = array('f',[ 0. ])

RTree = R.TTree('align','align')
RTree.Branch('filX', filX, 'filX/I')
RTree.Branch('filY', filY, 'filY/I')
RTree.Branch('x',x,'x/F')
RTree.Branch('y',y,'y/F')
RTree.Branch('pixX',pixX,'pixX/F')
RTree.Branch('pixY',pixY,'pixY/F')
RTree.Branch('edge',edge,'edge/I')
RTree.Branch('desig',desig,'desig/I')
#RTree.Branch('fidX',fidX,'fidX/F')
#RTree.Branch('fidY',fidY,'fidY/F')
#RTree.Branch('TfidX',TfidX,'fidX/F')
#RTree.Branch('TfidY',TfidY,'fidX/F')
#RTree.Branch('BfidX',BfidX,'fidX/F')
#RTree.Branch('BfidY',BfidY,'fidX/F')
RTree.Branch('fidX',fidX,'fidX/F')
RTree.Branch('fidY',fidY,'fidY/F')

with open(alignDataFiles) as data:
  for line in data: 
    d = line.split()
    j = 0             
    while j < len(d):
      if 'Calibration' in d[j]:
        mmX = float(d[j+4])
        mmY = float(d[j+6])
      if 'Number' in d[j]:
        lastFilX = int(d[j+4])
        lastFilY = int(d[j+6])
      if 'Size' in d[j]:
        stepX = float(d[j+4])
        stepY = float(d[j+6])
      if 'Initial' in d[j]:
        psX0 = float(d[j+6])
        psY0 = float(d[j+8])
      j += 1

with open(alignDataFiles, "r") as iv:            
            txtLines = [line for line in iv]
	    print "Reading headers..."
            idx = [i for i, line in enumerate(txtLines) if "fil" in line][0]
            headers = txtLines[idx].replace('\n','').replace('\r','').split('\t')
	    #print headers, data is reprersented as (idx[index], txtLines[data))
            #print mmX, mmY, stepX, stepY

            filX_idx = my_index(headers,"filx")
            filY_idx = my_index(headers,"fily")
            x_idx = my_index(headers,"psx")
            y_idx = my_index(headers,"psy")
            pixX_idx = my_index(headers,"pixx")
            pixY_idx = my_index(headers,"pixy")
            edge_idx = my_index(headers,"edge")
            desig_idx = my_index(headers,"f/e")

            #psXlist = [[],[],[],[]]
            #psYlist = [[],[],[],[]]
	    #crnrs = [[],[],[],[]]
	    #crnrxy = [[],[],[],[]]
            #pixX = []
            #pixY = []
            #edge = []
            #desig = []

            
	    #dzdx = -.0009
	    #dzdy = .0005

            data = txtLines[idx+1:]
	    print "Reading data..."

	    #lastcornerFid = [0,0,0,0]
	    #lastcornerEdg = [0,0,0,0]
	    #lastcornerxy = [0,0]
	    linenum = 0
	    TLcorner = []
	    TRcorner = [0,0]
	    BLcorner = [0,0]
	    BRcorner = [0,0]
	    #lastedge = -1
            #lastxy = -1

            for line in data:
              words = line.replace('\n','').replace('\r','').split('\t')
	      #print words
	      if len(words)>4:
                edge[0]=int(readvar(words,edge_idx))
		filX[0]=int(readvar(words,filX_idx))
                filY[0]=int(readvar(words,filY_idx))
                x[0]=(psX0-readvar(words,x_idx))*12.7
                y[0]=(readvar(words,y_idx)-psY0)*12.7
                pixX[0]=readvar(words,pixX_idx)
                pixY[0]=readvar(words,pixY_idx)
                desig[0]=int(readvar(words,desig_idx))
                fidX[0] = x[0]+pixX[0]*mmX
	        fidY[0] = y[0]+pixY[0]*mmY
                #z[0]=10160-readvar(words,z_idx)+(x[0]-x0)*dzdx + (y[0]-y0)*dzdy
                #print edge[0], "fidX", fidX[0], "fidY", fidY[0]
                #else: firstedge = 3	
                #if filY[0]==lastFilY and filX[0]==0 and desig[0]==33:
                #   lastedge = pixX[0]
                #else: lastedge = 3
                #print "firstedge is ",firstedge, "last edge is ",lastedge
                #print edgX[0]
                
		#if (edge[0] == lastedge): #(filX[0]==lastfilX and filY[0]==lastfilY 
		 #   lastcornerxy = [psX[0],psY[0]]
		  #  if (desig[0]==55):
		#	lastcornerFid = [psX[0],psY[0],fidX[0],fidY[0]]
		 #   if (desig[0]==33):
		#	lastcornerEdg = [psX[0],psY[0],edgX[0],edgY[0]]

		#print edge[0], lastedge, psX[0], psY[0], lastcorner
		#if (edge[0] != lastxy):
		#	crnrxy[edge[0]].append([psX[0],psY[0]])
		#	if (lastxy>=0): crnrxy[lastxy].append(lastcornerxy)
		#if (edge[0] != lastedge) and (desig[0]==55): #goodpt[0]>0): 
		#	crnrs[edge[0]].append([psX[0],psY[0],fidX[0],fidY[0]])
		#	if lastedge>=0: crnrs[lastedge].append(lastcornerFid)
		#if (edge[0] != lastedge) and (desig[0]==33): #goodpt[0]>0): 
		#	crnrs[edge[0]].append([psX[0],psY[0],edgX[0],edgY[0]])
		#	if lastedge>=0: crnrs[lastedge].append(lastcornerEdg)
		#if (desig[0]>0): #(goodpt[0]>0):
		#	lastedge = edge[0]
		#lastxy = edge[0]

		#psXlist[edge[0]].append(fidX[0])
		#psYlist[edge[0]].append(fidY[0])
		#psXlist[edge[0]].append(edgX[0])
		#psXlist[edge[0]].append(edgX[0])
		RTree.Fill()
		linenum += 1

	    #crnrs[lastedge].append(lastcornerEdg)
	    #crnrs[lastedge].append(lastcornerFid)
	    #crnrxy[lastxy].append(lastcornerxy)
	    print "File Reading complete"
	    #print "Corners Fiducials", crnrs
	    #print "Corners XY", crnrxy


if os.path.isfile(nameForSave+".root"): RFile = R.TFile(nameForSave+".root",'UPDATE')
else: RFile = R.TFile(nameForSave+".root",'RECREATE')
RTree.Write("",R.TObject.kOverwrite)

Z1 = R.TCanvas( 'Plots', 'Plots', 0, 0, 400, 400 )
#c1.SetTitle(prefix+"_qvt")
Z1.Divide(2,2)
Z1.Update()

RFit = R.TF1()
fiducials = []
fiducialserr = []
fiducialsY = []
edges = []
edgeserr = []
edgesY = []
#flatZ = []
#flatZerr = []
TGrX = []
TGrY = []
YGrX = []
YGrY = []
UGrX = []
UGrY = []
IGrY = []
IGrX = []
TopEGr = []
TopFGr = []
BotEGr = []
BotFGr = []


for i in xrange(4):    
	RTree.Draw("fidY:fidX","edge==" + str(i) + "&& desig==55")
	FGr = R.TGraph(RTree.GetSelectedRows(), RTree.GetV2(), RTree.GetV1())
        FGr.SetName("fid at edge " + str(i))
        FGr.SetTitle("Fiducials")
        FGr.SetMarkerColor(1)
        FGr.SetLineColor(4) #4 = blue
        FGr.GetXaxis().SetTitle("x (um)")
        FGr.GetYaxis().SetTitle("y (um)")
        FGr.Draw("*")
        FGr.Fit("pol1")
	if FGr.GetN() != 0: FGr.GetFunction("pol1").SetLineColor(4) #check if this work
        fiducials.append(R.gROOT.GetFunction("pol1").GetParameter(1))
        fiducialsY.append(R.gROOT.GetFunction("pol1").GetParameter(0))
        fiducialserr.append(R.gROOT.GetFunction("pol1").GetParError(1))
        FGr.Write("",R.TObject.kOverwrite)
        Z1.SaveAs(nameForSave+"_fidatedge_" + str(i) + ".jpg")

        if (i == 1 or i ==2): RTree.Draw("fidX:fidY","edge==" + str(i) + "&& desig==33")
	else: RTree.Draw("fidY:fidX","edge==" + str(i) + "&& desig==33")
	EGr = R.TGraph(RTree.GetSelectedRows(), RTree.GetV2(), RTree.GetV1())
        EGr.SetName("edge at edge " + str(i))
        EGr.SetTitle("Edges")
        EGr.SetMarkerColor(1)
        EGr.SetLineColor(2) #2 = red
        if (i == 1 or i == 2):
          EGr.GetXaxis().SetTitle("y (um)")
          EGr.GetYaxis().SetTitle("x (um)")
        else:
          EGr.GetXaxis().SetTitle("x (um)")
          EGr.GetYaxis().SetTitle("y (um)")
        EGr.Draw("*")
        EGr.Fit("pol1")
	EGr.GetFunction("pol1").SetLineColor(2) #check if this work
        edges.append(R.gROOT.GetFunction("pol1").GetParameter(1))
        edgesY.append(R.gROOT.GetFunction("pol1").GetParameter(0))
        edgeserr.append(R.gROOT.GetFunction("pol1").GetParError(1))
        EGr.Write("",R.TObject.kOverwrite)
        Z1.SaveAs(nameForSave+"_edgeatedge_" + str(i) + ".jpg")

#The following Tree is to obtain each individual corner on the sensor
RTree.Draw("fidY:fidX", "filX==0" + "&& filY==0" + "&& desig==33") #to get corner coordinates
TGr = R.TGraph(RTree.GetSelectedRows(), RTree.GetV2(), RTree.GetV1())
TGr.SetName("TL corner")
TGr.SetTitle("TLCorner")
TGr.SetMarkerColor(2)
TGr.SetLineColor(2)
TGr.GetXaxis().SetTitle("x (um)")
TGr.GetYaxis().SetTitle("y (um)")
TGr.Draw("*P")
TGrX = (fidX.tolist())
TGrY = (fidY.tolist())
TGr.Write("",R.TObject.kOverwrite)
#Z1.SaveAs(nameForSave+"_TLcorner" ".jpg")

RTree.Draw("fidY:fidX", "filX==0" + "&& filY==" + str(int(lastFilY)) + "&& desig==33")
YGr = R.TGraph(RTree.GetSelectedRows(), RTree.GetV2(), RTree.GetV1())
YGr.SetName("BL corner")
YGr.SetTitle("BLCorner")
YGr.SetMarkerColor(5)
YGr.SetLineColor(5)
YGr.GetXaxis().SetTitle("x (um)")
YGr.GetYaxis().SetTitle("y (um)")
YGr.Draw("*P")
YGrX = (fidX.tolist())
YGrY = (fidY.tolist())
YGr.Write("",R.TObject.kOverwrite)
#Z1.SaveAs(nameForSave+"_BLcorner" ".jpg")

RTree.Draw("fidY:fidX", "filX==" + str(int(lastFilX)) + "&& filY==0" + "&& desig==33")
UGr = R.TGraph(RTree.GetSelectedRows(), RTree.GetV2(), RTree.GetV1())
UGr.SetName("TR corner")
UGr.SetTitle("TRCorner")
UGr.SetMarkerColor(3)
UGr.SetLineColor(3)
UGr.GetXaxis().SetTitle("x (um)")
UGr.GetYaxis().SetTitle("y (um)")
UGr.Draw("*P")
UGrX = (fidX.tolist())
UGrY = (fidY.tolist())
UGr.Write("",R.TObject.kOverwrite)

RTree.Draw("fidY:fidX", "filX==" + str(int(lastFilX)) + "&& filY==" + str(int(lastFilY)) + "&& desig==33")
IGr = R.TGraph(RTree.GetSelectedRows(), RTree.GetV2(), RTree.GetV1())
IGr.SetName("BR corner")
IGr.SetTitle("BRCorner")
IGr.SetMarkerColor(4)
IGr.SetLineColor(4)
IGr.GetXaxis().SetTitle("x (um)")
IGr.GetYaxis().SetTitle("y (um)")
IGr.Draw("*P")
IGrX = (fidX.tolist())
IGrY = (fidY.tolist())
IGr.Write("",R.TObject.kOverwrite)

print "Coordinates (X,Y): TL= ", TGrX, TGrY, "BL= ", YGrX, YGrY, "TR= ", UGrX, UGrY, "BR= ", IGrX, IGrY

#RTree.Draw("fidY:fidX", "desig==33")
#OGr = R.TGraph(RTree.GetSelectedRows(), RTree.GetV2(), RTree.GetV1())
#OGr.SetName("BR corner")
#OGr.SetTitle("BRCorner")
#OGr.SetMarkerColor(2)
#OGr.SetLineColor(2)
#OGr.GetXaxis().SetTitle("x (um)")
#OGr.GetYaxis().SetTitle("y (um)")
#OGr.Draw("*LP")
#OGrX = (fidX.tolist())
#OGrY = (fidY.tolist())
#OGr.Write("",R.TObject.kOverwrite)

Z1.Update()

#Z1.SaveAs(nameForSave+"_zProfile.jpg")

print "\nSlope of Edges"
print "edges = ", edges, "\nedgeserr = ", edgeserr, "\nfiducials = ", fiducials, "\nfiducialserr = ", fiducialserr


#ChuckMap = R.TH2F("ChuckMap","Chuck Z height",10,121500,211500,10,58500,148500)
#RTree.Draw("x:y>>ChuckMap","z","colz")
#ChuckMap.Write("",R.TObject.kOverwrite)

#print "Flatness"
#print flatZ
#print flatZerr

#print "Corner Fiducials" 
#for i in xrange(4): 
#	print crnrs[i]

#corners = [[[0,0],[0,0]],[[0,0],[0,0]],[[0,0],[0,0]],[[0,0],[0,0]]]

#print "Corners (edges)"
#corners[0][0] = [crnrs[0][0][3]+crnrxy[0][0][0]-crnrs[0][0][0]-pss_xoff, crnrs[0][0][4]+crnrxy[0][0][1]-crnrs[0][0][1]+pss_yoff]
#corners[1][0] = [crnrs[1][0][3]+crnrxy[1][0][0]-crnrs[1][0][0]-psp_xoff, crnrs[1][0][4]+crnrxy[1][0][1]-crnrs[1][0][1]+psp_yoff]
#corners[2][0] = [crnrs[2][0][3]+crnrxy[2][0][0]-crnrs[2][0][0]-psp_xoff, crnrs[2][0][4]+crnrxy[2][0][1]-crnrs[2][0][1]-psp_yoff]
#corners[3][0] = [crnrs[3][0][3]+crnrxy[3][0][0]-crnrs[3][0][0]-pss_xoff, crnrs[3][0][4]+crnrxy[3][0][1]-crnrs[3][0][1]-pss_yoff]
#corners[0][1] = [crnrs[0][1][3]+crnrxy[0][1][0]-crnrs[0][1][0]+pss_xoff, crnrs[0][1][4]+crnrxy[0][1][1]-crnrs[0][1][1]+pss_yoff]
#corners[1][1] = [crnrs[1][1][3]+crnrxy[1][1][0]-crnrs[1][1][0]+psp_xoff, crnrs[1][1][4]+crnrxy[1][1][1]-crnrs[1][1][1]+psp_yoff]
#corners[2][1] = [crnrs[2][1][3]+crnrxy[2][1][0]-crnrs[2][1][0]+psp_xoff, crnrs[2][1][4]+crnrxy[2][1][1]-crnrs[2][1][1]-psp_yoff]
#corners[3][1] = [crnrs[3][1][3]+crnrxy[3][1][0]-crnrs[3][1][0]+pss_xoff, crnrs[3][1][4]+crnrxy[3][1][1]-crnrs[3][1][1]-pss_yoff]

#distS = []
#distL = []
#for i in xrange(4): 
#	print corners[i]
#	if i<3: j = i+1
#	else: j = 0
#	distS.append(((corners[i][0][0]-corners[i][1][0])**2+(corners[i][0][1]-corners[i][1][1])**2)**0.5)

#for i in xrange(2): 
#	if i == 0:  j = 3
#	else: j = 1
#	distL.append(((corners[2*i][0][0]-corners[j][0][0])**2+(corners[2*i][0][1]-corners[j][0][1])**2)**0.5)
#	distL.append(((corners[2*i][1][0]-corners[j][1][0])**2+(corners[2*i][1][1]-corners[j][1][1])**2)**0.5)

#deltaZ = [crnrs[0][0][2]-crnrs[1][0][2], crnrs[0][1][2]-crnrs[1][1][2], crnrs[3][0][2]-crnrs[2][0][2], crnrs[3][1][2]-crnrs[2][1][2]]
#overhang = [corners[0][0][1]-corners[1][0][1], corners[0][1][1]-corners[1][1][1], corners[3][0][1]-corners[2][0][1], corners[3][1][1]-corners[2][1][1]]
#shift = [corners[0][0][0]-corners[1][0][0], corners[0][1][0]-corners[1][1][0], corners[3][0][0]-corners[2][0][0], corners[3][1][0]-corners[2][1][0]]
#print "Overhangs: ", overhang
#print "Shifts: ", shift
#print "Delta Z:", deltaZ

#print "Dimensions:"
#print "\t\t",distS[1]
#print "\t\t",distS[0]
#print "PSS: ",distL[0],"\t",distL[1]
#print "PSP: ",distL[2],"\t",distL[3]
#print "\t\t",distS[3]
#print "\t\t",distS[2]

#print "\n","Offsets:"
#overhang = [corners[0][0][1]-corners[1][0][1], corners[0][1][1]-corners[1][1][1], corners[3][0][1]-corners[2][0][1], corners[3][1][1]-corners[2][1][1]]
#shift = [corners[0][0][0]-corners[1][0][0], corners[0][1][0]-corners[1][1][0], corners[3][0][0]-corners[2][0][0], corners[3][1][0]-corners[2][1][0]]
#print "Overhangs: ", overhang
#print "Shifts: ", shift
#print "Delta Z:", deltaZ

#print "Dimensions:"
#print "\t\t",distS[1]
#print "\t\t",distS[0]
#print "PSS: ",distL[0],"\t",distL[1]
#print "PSP: ",distL[2],"\t",distL[3]
#print "\t\t",distS[3]
#print "\t\t",distS[2]

#print "\n","Offsets:"
#print "\n","Offsets:"
#print "\t", overhang[0], overhang[1], "\t"
#print shift[0], "\t\t", shift[1] 
#print shift[2], "\t\t", shift[3] 
#print "\t", overhang[2], overhang[3], "\t"

#print "\nSlope of Edges"
#print edges[0], edges[1], edges[2], edges[3]
#print "Error in Fit:"
#print edgeserr

#zPSS = R.TMultiGraph()
#zPSS.SetName("zPSS")
#zPSS.SetTitle("PSS Z Profile")
#zPSS.GetXaxis().SetTitle("x Pos (um)")
#zPSS.GetYaxis().SetTitle("z Pos (um)")
#zPSP = R.TMultiGraph()
#zPSP.SetName("zPSP")
#zPSP.SetTitle("PSP Z Profile")
#zPSP.GetXaxis().SetTitle("x Pos (um)")
#zPSP.GetYaxis().SetTitle("z Pos (um)")

#zPSS.Add(RFile.Get("Z Edge 0"))
#zPSS.Add(RFile.Get("Z Edge 3"))

#zPSP.Add(RFile.Get("Z Edge 1"))
#zPSP.Add(RFile.Get("Z Edge 2"))



TopEdge = (R.TMath.ATan(fiducials[0]) - R.TMath.ATan(edges[0]))*1000000
BotEdge = (R.TMath.ATan(edges[3]) - R.TMath.ATan(fiducials[3]))*1000000
TopEdgeS = abs(edgesY[0] - fiducialsY[0])
BotEdgesS = abs(edgesY[3] - fiducialsY[3])

TopBottomEdge = ((R.TMath.ATan(edges[3])) - (R.TMath.ATan(edges[0])))*1000000
LeftRightEdge = ((R.TMath.ATan(edges[2])) - (R.TMath.ATan(edges[1])))*1000000

TopTitle = "Top Fid Edge Parallelism " + str(int(TopEdge)) + " urad" #micro-radians
BotTitle = "Bottom Fid Edge Parallelism " + str(int(BotEdge)) + " urad"

TopBottomTitle = "Top Bottom Edge Parallelism " + str(int(TopBottomEdge)) + " urad" #micro-radians
LeftRightTitle = "Left Right Edge Parallelism " + str(int(LeftRightEdge)) + " urad" #micro-radians
print TopTitle, BotTitle
print TopBottomTitle, LeftRightTitle

Top2 = float((((TGrX[0] - UGrX[0]))**2 + ((TGrY[0] - UGrY[0]))**2)**(1/2)) 
Bottom2 = float((((YGrX[0] - IGrX[0]))**2 + ((YGrY[0] - IGrY[0]))**2)**(1/2))
Left2 = float((((TGrX[0] - YGrX[0]))**2 + ((TGrY[0] - YGrY[0]))**2)**(1/2))
Right2 = float((((UGrX[0] - IGrX[0]))**2 + ((UGrY[0] - IGrY[0]))**2)**(1/2))
print "Length Uncalibrated: ", " Top:" , Top2 , " Bot:" , Bottom2 , " Left:"  ,Left2 , " Right:", Right2

Top = ( (Top2) - ((Top2)**2)*(0.0000000119442) + (Top2)*0.002361)
Bottom = ( (Bottom2) - ((Bottom2)**2)*(0.0000000119442) + (Bottom2)*0.002361)
Left = ( (Left2) + ((Left2)**2)*(0.000000007) + (Left2)*0.0004)
Right = ( (Right2) + ((Right2)**2)*(0.000000007) + (Right2)*0.0004)
print "Length Calibrated: ", "TopCalibrated: ", Top, " BottomCalibrated:", Bottom, " LeftCalib:", Left, " RightCalib: ", Right


TLcorner = R.TMath.ACos(((TGrX[0]-UGrX[0])*(TGrX[0]-YGrX[0]) + (TGrY[0]-UGrY[0])*(TGrY[0]-YGrY[0]))/(Top*Left))*(180/(R.TMath.Pi()))
TRcorner = R.TMath.ACos(((UGrX[0]-TGrX[0])*(UGrX[0]-IGrX[0]) + (UGrY[0]-TGrY[0])*(UGrY[0]-IGrY[0]))/(Top*Right))*(180/(R.TMath.Pi()))
BLcorner = R.TMath.ACos(((YGrX[0]-TGrX[0])*(YGrX[0]-IGrX[0]) + (YGrY[0]-TGrY[0])*(YGrY[0]-IGrY[0]))/(Bottom*Left))*(180/(R.TMath.Pi()))
BRcorner = R.TMath.ACos(((IGrX[0]-UGrX[0])*(IGrX[0]-YGrX[0]) + (IGrY[0]-UGrY[0])*(IGrY[0]-YGrY[0]))/(Bottom*Right))*(180/(R.TMath.Pi()))

print "TopLeftcorner ", TLcorner, "TopRightcorner ", TRcorner, "BottomLeftcorner ", BLcorner, "BottomRight corner ", BRcorner

GrTop = R.TMultiGraph()
GrTop.SetName("Top Fid Edge")
GrTop.SetTitle("Top Fid Edge Parallelism: " + str(int(TopEdge)) + "urad" + " Separation: " + str(float(TopEdgeS)) +"um")
#GrTop.GetXaxis().SetTitle("x Pos (um)")
#GrTop.GetYaxis().SetTitle("y Pos (um)")
GrBot = R.TMultiGraph()
GrBot.SetName("Bottom Fid Edge")
GrBot.SetTitle("Bottom Fid Edge Parallelism: " + str(int(BotEdge)) + "urad" + " Separation: " + str(float(BotEdgesS)) + "um")
#GrBot.GetXaxis().SetTitle("x Pos (um)")
#GrBot.GetYaxis().SetTitle("y Pos (um)")

c3 = R.TCanvas( 'Fiducials', 'Fiducials', 0, 0, 1200, 1200 )
c3.Divide(1,2)

c3.cd(1)
GrTop.Add(RFile.Get("edge at edge 0"))
GrTop.Add(RFile.Get("fid at edge 0"))
GrTop.Draw("*A")
#c3.SaveAs(nameForSave+"_TopFidEdgeParal.jpg")

legend3 = R.TLegend(0.1, 0.75, 0.3, 0.9)
legend3.SetHeader("Error (microns)")
legend3.AddEntry("GrTop", "edgeErr(red): "+ str(int(edgeserr[0]*1000000)))
legend3.AddEntry("GrTop", "fidErr(blue): "+ str(int(fiducialserr[0]*1000000)))
legend3.Draw()

c3.cd(2)
GrBot.Add(RFile.Get("fid at edge 3"))
GrBot.Add(RFile.Get("edge at edge 3"))
GrBot.Draw("*A")
#c3.Update()

#zPSS.Write("",R.TObject.kOverwrite)
#zPSP.Write("",R.TObject.kOverwrite)

#legend2 = R.TLegend(0.1, 0.1, 0.3, 0.3)
legend2 = R.TLegend(0.1, 0.75, 0.3, 0.9)
legend2.SetHeader("Error (microns)")
legend2.AddEntry("GrBot", "edgeErr(red): "+ str(int(edgeserr[3]*1000000)))
legend2.AddEntry("GrBot", "fidErr(blue): "+ str(int(fiducialserr[3]*1000000)))
legend2.Draw()

c3.SaveAs(nameForSave+"_FidEdgeParallel.jpg")

GrTop.Write("",R.TObject.kOverwrite)
GrBot.Write("",R.TObject.kOverwrite)


Z1.Write("",R.TObject.kOverwrite)
#c2.Write("zProfile",R.TObject.kOverwrite)
#c3.Write("",R.TObject.kOverwrite)

Grtop = R.TMultiGraph()
Grtop.SetName("Top Edge")
Grtop.SetTitle("Top Edge & TopBotParallelism: " + str(int(TopBottomEdge)) + " urad")

Grbot = R.TMultiGraph()
Grbot.SetName("Bottom Edge")
Grbot.SetTitle("Bottom Edge")

Grlef = R.TMultiGraph()
Grlef.SetName("Left Edge")
Grlef.SetTitle("Left Edge & LeftRightParallelism: " + str(int(LeftRightEdge)) + " urad")

Grrit = R.TMultiGraph()
Grrit.SetName("Right Edge")
Grrit.SetTitle("Right Edge")

c5 = R.TCanvas( 'EdgeEdge', 'EdgeEdge', 0, 0, 1200, 1200 )
c5.Divide(2,2)

c5.cd(1)
Grtop.Add(RFile.Get("edge at edge 0"))
Grtop.Draw("*A")

legend4 = R.TLegend(0.1, 0.7, 0.4, 0.9)
legend4.SetHeader("Error (microns)")
legend4.AddEntry("GrTopBot", "TopErr: "+ str(int((edgeserr[0])*1000000)))
legend4.Draw()

c5.cd(2)
Grbot.Add(RFile.Get("edge at edge 3"))
Grbot.Draw("*A")

legend6 = R.TLegend(0.1, 0.7, 0.4, 0.9)
legend6.SetHeader("Error (microns)")
legend6.AddEntry("GrTopBot", "BotErr: "+ str(int((edgeserr[3])*1000000)))
legend6.Draw()

c5.cd(3)
Grlef.Add(RFile.Get("edge at edge 1"))
Grlef.Draw("*A")

legend5 = R.TLegend(0.1, 0.1, 0.4, 0.3)
legend5.SetHeader("Error (microns)")
legend5.AddEntry("GrLefRit", "LeftErr: "+ str(int((edgeserr[1])*1000000)))
legend5.Draw()

c5.cd(4)
Grrit.Add(RFile.Get("edge at edge 2"))
Grrit.Draw("*A")

legend7 = R.TLegend(0.1, 0.1, 0.4, 0.3)
legend7.SetHeader("Error (microns)")
legend7.AddEntry("GrLefRit", "RightErr: "+ str(int((edgeserr[2])*1000000)))
legend7.Draw()

c5.SaveAs(nameForSave+"_EdgeEdgeParallel.jpg")

Grtop.Write("",R.TObject.kOverwrite)
Grbot.Write("",R.TObject.kOverwrite)
Grlef.Write("",R.TObject.kOverwrite)
Grrit.Write("",R.TObject.kOverwrite)

GrCor = R.TMultiGraph()
GrCor.SetName("Lengths")
GrCor.SetTitle("Length(um):  " + "Top:" + str(Top) + "  Bot:" + str(Bottom) + "  Left:" + str(Left) + "  Right:" + str(Right))

c4 = R.TCanvas( 'Corners', 'Corners', 0, 0, 1200, 1200 )
#c4.Divide(1,2)
#c4.cd(1)

GrCor.Add(RFile.Get("TL corner"))
GrCor.Add(RFile.Get("TR corner"))
GrCor.Add(RFile.Get("BR corner"))
GrCor.Add(RFile.Get("BL corner"))
GrCor.Draw("*A")

legend = R.TLegend(0.5,0.5, 0.8,0.8)
legend.SetHeader("Corner(degrees)")
legend.AddEntry("TGr","TLcorner: " + str(float(TLcorner)))
legend.AddEntry("YGr","BLcorner: " + str(float(BLcorner))) 
legend.AddEntry("UGr","TRcorner: " + str(float(TRcorner))) 
legend.AddEntry("IGr","BRcorner: " + str(float(BRcorner))) 
legend.Draw()

c4.SaveAs(nameForSave+"_lengths.jpg")
GrCor.Write("",R.TObject.kOverwrite)

#c2 = R.TCanvas( 'Z Profile', 'Z Profile', 0, 0, 400, 400 )
#c2 = R.TCanvas()
#R.gStyle.SetOptStat(0)
#c2.Clear()
#c2.Divide(1,2)
#c2.Update()
#Z1.Update()
#Z1.cd(1) 
#zPSS.Draw()
#RFile.Get("zPSS").Draw()
#c2.cd(2)
#zPSP.Draw()
#Z1.Update()
#Z1.SaveAs(nameForSave+"_zProfile.jpg")

RFile.Close()

#for i in xrange(4):
#	end = len(xlist[i])

rootFile = R.TFile()

textfile = open(nameForSave+"_summary.txt", "w")
textfile.write (nameForSave)
textfile.write ("\n")
textfile.write ("\n")
textfile.write ("Parallelism (micro-radians):\n")
textfile.write ("Top Fiducials and Edge:    " + str(TopEdge) + " urad\n")
textfile.write ("Bottom Fiducials and Edge: " + str(BotEdge) + " urad\n")
textfile.write ("Top and Bottom Edge:       " + str(TopBottomEdge) + " urad\n")
textfile.write ("Left and Right Edge:       " + str(LeftRightEdge) + " urad\n")
textfile.write ("\n")
textfile.write ("Length of Edges:\n")
textfile.write ("Top:    " + str(Top) +" microns\n")
textfile.write ("Left:   " + str(Left) + " microns\n")
textfile.write ("Right:  " + str(Right) + " microns\n")
textfile.write ("Bottom: " + str(Bottom) + " microns\n")
textfile.write ("\n")
textfile.write ("Avg Displacement of Edge and Fiducials:\n")
textfile.write ("Top:    " + str(TopEdgeS) + " microns\n")
textfile.write ("Bottom: " + str(BotEdgesS) + " microns\n")
textfile.write ("\n")
textfile.write ("Corners Perpendicularism:\n")
textfile.write ("TopLeft:     " + str(TLcorner) + " degrees\n")
textfile.write ("TopRight:    " + str(TRcorner) + " degrees\n")
textfile.write ("BottomLeft:  " + str(BLcorner) + " degrees\n")
textfile.write ("BottomRight: " + str(BRcorner) + " degrees\n")
textfile.write ("\n")
textfile.write ("ERRORS:\n")
textfile.write ("Edges:\n")
textfile.write ("Edge Top:    " + str(float(edgeserr[0]*1000000)) + " microns\n")
textfile.write ("Edge Left:   " + str(float(edgeserr[1]*1000000)) + " microns\n")
textfile.write ("Edge Right:  " + str(float(edgeserr[2]*1000000)) + " microns\n")
textfile.write ("Edge Bottom: " + str(float(edgeserr[3]*1000000)) + " microns\n")
textfile.write ("Fiducials:\n")
textfile.write ("Fid Top:     " + str(float(fiducialserr[0]*1000000)) + " microns\n")
textfile.write ("Fid Bottom:  " + str(float(fiducialserr[3]*1000000)) + " microns\n")
textfile.write ("\n")
textfile.write ("Calibration (um/pixel):\n")
textfile.write ("X: " + str(mmX) + " microns")
textfile.write ("\n")
textfile.write ("Y: " + str(mmY) + " microns")
#textfile.write ("PSP Fiducial Offset: (" + str(psp_xoff) + ", " + str(psp_yoff) + ")\n")
#textfile.write ("\n")
#textfile.write ("Corners Silicon:\n")
#for i in corners: textfile.write(str(i)+"\n")
#textfile.write ("\n")
#textfile.write ("Overhangs:\n")
#for i in overhang: textfile.write(str(i)+"\n")
#textfile.write ("\n")
#textfile.write ("Shift:\n")
#for i in shift: textfile.write(str(i)+"\n")
#textfile.write ("\n")
#textfile.write ("Delta Z:\n")
#for i in deltaZ: textfile.write(str(i)+"\n")
textfile.close()
