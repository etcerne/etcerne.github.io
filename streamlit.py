import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import seaborn as sns




def parse(data):
    game_df= pd.read_csv(data)
    return game_df

st.title("Pomona-Pitzer Baseball Analysis")

st.write("This app allows you to analyze pitchers using their Trackman data. First, upload the csv files of the games you would like to" \
" analyze. You may upload as many files as you want. Select a team and a pitcher from that team. You will then be able to see the metrics on each of their pitches," \
" as well as a pie chart showing the frequency with which they throw each of their pitches." \
"")

st.write(" You can also view each individual pitch that the pitcher through in the csv files you uploaded." \
" Additionally, you can see a pitch chart where each individual pitch is graphed. Check the 'Analyze By Count' box to find out" \
" how a pitcher's pitch usage changes depending on the count. You can also view a pitcher's " \
" whiff rate, hard hit rate, ground ball rate and first pitch strike rate by checking the 'See Advanced Statistics' box." \
" Finally, you can perform PCA analyses on all of the pitchers on the team you've selected, or on each of their individual" \
" pitches.")


st.logo('ppbaseball.jpg')


parsed_files_list=[]
with st.sidebar:
    files=st.file_uploader("Upload files here",type=["csv"],accept_multiple_files=True)
for i in range(len(files)):
    parsed_files_list=parsed_files_list+[parse(files[i])]

if not files:
    st.write("Time to explore the app!")
    st.stop()

all_files_merged=pd.concat(parsed_files_list)
full_df=pd.DataFrame(all_files_merged)


analysis_selection=st.multiselect("What would you like to analyze?",('RelSpeed','SpinRate','SpinAxis','InducedVertBreak',
                                                                   'HorzBreak','Extension',"VertApprAngle","HorzApprAngle"))

pick_team=st.selectbox("Which team would you like to analyze?",(full_df["PitcherTeam"].unique()))
full_df=full_df.loc[full_df["PitcherTeam"]==pick_team]


pitchers=full_df.groupby("Pitcher")["RelSpeed"].mean()
pitcher_selection=st.selectbox("Which pitcher would you like to analyze?",(pitchers.index))

dfs_list=[]

all_data=st.checkbox('Select all statistics',value=True)
if not all_data and not analysis_selection:
    st.write("Please check the box above or select a statistic from the dropdown menu above.")
    st.stop()
if all_data:
    analysis_selection=('RelSpeed','SpinRate','SpinAxis','InducedVertBreak',
                                                                   'HorzBreak','Extension','VertApprAngle',"HorzApprAngle")


all_pitches=full_df.loc[full_df["Pitcher"]==f"{pitcher_selection}"]
date=all_pitches.groupby("Date")["RelSpeed"].mean()
date_selection=pd.DataFrame
all_pitches.drop(columns=["Tilt","PitcherThrows","Time","PAofInning","PitchofPA",
                                                        "PitcherId","PitcherTeam","Batter","BatterId","BatterSide","BatterTeam",
                                                        "PitcherSet","Inning","Top/Bottom","Outs",
                                                        "AutoPitchType","KorBB","TaggedHitType","PlayResult",
                                                        "OutsOnPlay","RunsScored","Notes","Direction","HitSpinRate","PositionAt110X","PositionAt110Y","PositionAt110Z","Distance","LastTrackedDistance","Bearing",
                                                        "HangTime","pfxx","pfxz","x0","y0","z0","vx0","vy0","vz0","ax0","ay0","az0","HomeTeam","AwayTeam","Stadium","Level","League","GameID","PitchUID","EffectiveVelo","MaxHeight",'MeasuredDuration','SpeedDrop','PitchLastMeasuredX',
                                                        "PitchLastMeasuredY","PitchLastMeasuredZ","ContactPositionX","ContactPositionY","ContactPositionZ","GameUID","UTCDate","UTCTime","LocalDateTime","UTCDateTime","AutoHitType","System","HomeTeamForeignID",
                                                        "AwayTeamForeignID","GameForeignID","Catcher","CatcherId","CatcherThrows","CatcherTeam","PlayID","PitchTrajectoryXc0","PitchTrajectoryXc1","PitchTrajectoryXc2","PitchTrajectoryYc0","PitchTrajectoryYc1",
                                                        "PitchTrajectoryYc2","PitchTrajectoryZc0","PitchTrajectoryZc1","PitchTrajectoryZc2","HitSpinAxis","HitTrajectoryXc0","HitTrajectoryXc1","HitTrajectoryXc2","HitTrajectoryXc3","HitTrajectoryXc4",
                                                        "HitTrajectoryXc5","HitTrajectoryXc6","HitTrajectoryXc7","HitTrajectoryXc8","HitTrajectoryYc0","HitTrajectoryYc1","HitTrajectoryYc2","HitTrajectoryYc3","HitTrajectoryYc4","HitTrajectoryYc5","HitTrajectoryYc6",
                                                        "HitTrajectoryYc7","ThrowSpeed","HitTrajectoryYc8","HitTrajectoryZc0","HitTrajectoryZc1","HitTrajectoryZc2","HitTrajectoryZc3","HitTrajectoryZc4","HitTrajectoryZc5","HitTrajectoryZc6","HitTrajectoryZc7","HitTrajectoryZc8",
                                                        "PopTime","ExchangeTime","TimeToBase","CatchPositionX","CatchPositionY","CatchPositionZ","ThrowPositionX","ThrowPositionY","ThrowPositionZ","BasePositionX","BasePositionY","BasePositionZ","ThrowTrajectoryXc0","ThrowTrajectoryXc1",
                                                        "ThrowTrajectoryXc2","ThrowTrajectoryYc0","ThrowTrajectoryYc1","ThrowTrajectoryYc2","ThrowTrajectoryZc0","ThrowTrajectoryZc1","ThrowTrajectoryZc2","PitchReleaseConfidence","PitchLocationConfidence","PitchMovementConfidence",
                                                        "HitLaunchConfidence","HitLandingConfidence",
                                                        "CatcherThrowCatchConfidence","CatcherThrowReleaseConfidence","CatcherThrowLocationConfidence"],inplace=True)

all_pitches=all_pitches.reset_index()

for i in analysis_selection:
    df=pd.DataFrame(full_df.groupby(["Pitcher","TaggedPitchType"])[f'{i}'].mean().round(1))
    dfs_list=dfs_list+[df.loc[f'{pitcher_selection}']]
all_data=pd.concat(dfs_list,axis=1)
all_data["Pitcher"]=pitcher_selection  
types=all_pitches["TaggedPitchType"].unique()

pitch_usage=[]
for i in types: 
    counter=all_pitches.loc[all_pitches["TaggedPitchType"]==i]
    pitch_usage=pitch_usage+[len(counter)]
    pitch_usage_df=pd.DataFrame(pitch_usage)
    pitch_usage_df.columns=["Count"]

all_data.drop(columns=["Pitcher"],inplace=True)



types_df=pd.DataFrame(types)
almost=pd.concat([types_df,pitch_usage_df],axis=1)
almost.columns=["Pitch","Frequency"]
done=pd.merge(almost,all_data,left_on="Pitch",right_index=True)

total=sum(done["Frequency"])

done["Frequency"]=done["Frequency"]/total



st.write(done)

pitching=px.pie(done,values="Frequency",names="Pitch",title="Pitch Frequencies")
st.plotly_chart(pitching)


individual=st.checkbox("View Data on Individual Pitches")
if individual:
    st.write(f"All Pitches by {pitcher_selection}")


    st.write(all_pitches.drop(columns=["index"]))



pitch_chart=st.checkbox(f"View Pitch Chart")
if pitch_chart:

    pitches_visual=px.scatter(all_pitches,x="PlateLocSide",y="PlateLocHeight",color="TaggedPitchType",
                              title=f"Pitch Chart for {pitcher_selection}")
    pitches_visual.update_traces(marker_size=7.5)
    pitches_visual.add_shape(type="rect",x0=-0.7083,y0=3.355,x1=0.7083,y1=1.645,line=dict(color="orange"))
    pitches_visual.update_xaxes(range=[-4.5,4.5])
    pitches_visual.update_yaxes(range=[0,5])
    
    st.plotly_chart(pitches_visual)







count=st.checkbox("Analyze by Count")



if count:
    balls=st.selectbox("How many balls?",(0,1,2,3))
    strikes=st.selectbox("How many strikes?",(0,1,2))

    by_count=all_pitches.loc[(all_pitches["Balls"]==balls) & (all_pitches["Strikes"]==strikes)]
    by_count_df=pd.DataFrame(by_count)

    percentages=by_count_df.groupby("TaggedPitchType").count()
    percentages_df=pd.DataFrame(percentages)
    total=percentages_df["PitchNo"].sum()
    short=percentages_df.iloc[:,[0]]
    final_percentages=short/total
    final_percentages["Total"]=percentages_df["PitchNo"]
    final_percentages.columns=["Frequency","Total"]

    count_pie=px.pie(final_percentages,values="Frequency",names=final_percentages.index,title=f"Pitch Frequencies in a {balls}-{strikes} count")

    st.write(f"Total pitches thrown in a {balls}-{strikes} count:")
    st.write(f'{total}')
    st.write(final_percentages)
    st.plotly_chart(count_pie)

full_df_drop=full_df.drop(columns=["Tilt","TaggedPitchType","PitcherThrows","PitchNo","Date","Time","PAofInning","PitchofPA","Pitcher",
                                                        "PitcherId","PitcherTeam","Batter","BatterId","BatterSide","BatterTeam",
                                                        "PitcherSet","Inning","Top/Bottom","Outs","Balls","Strikes",
                                                        "AutoPitchType","PitchCall","KorBB","TaggedHitType","PlayResult",
                                                        "OutsOnPlay","RunsScored","Notes","ExitSpeed","Angle","Direction","HitSpinRate","PositionAt110X","PositionAt110Y","PositionAt110Z","Distance","LastTrackedDistance","Bearing",
                                                        "HangTime","pfxx","pfxz","x0","y0","z0","vx0","vy0","vz0","ax0","ay0","az0","HomeTeam","AwayTeam","Stadium","Level","League","GameID","PitchUID","EffectiveVelo","MaxHeight",'MeasuredDuration','SpeedDrop','PitchLastMeasuredX',
                                                        "PitchLastMeasuredY","PitchLastMeasuredZ","ContactPositionX","ContactPositionY","ContactPositionZ","GameUID","UTCDate","UTCTime","LocalDateTime","UTCDateTime","AutoHitType","System","HomeTeamForeignID",
                                                        "AwayTeamForeignID","GameForeignID","Catcher","CatcherId","CatcherThrows","CatcherTeam","PlayID","PitchTrajectoryXc0","PitchTrajectoryXc1","PitchTrajectoryXc2","PitchTrajectoryYc0","PitchTrajectoryYc1",
                                                        "PitchTrajectoryYc2","PitchTrajectoryZc0","PitchTrajectoryZc1","PitchTrajectoryZc2","HitSpinAxis","HitTrajectoryXc0","HitTrajectoryXc1","HitTrajectoryXc2","HitTrajectoryXc3","HitTrajectoryXc4",
                                                        "HitTrajectoryXc5","HitTrajectoryXc6","HitTrajectoryXc7","HitTrajectoryXc8","HitTrajectoryYc0","HitTrajectoryYc1","HitTrajectoryYc2","HitTrajectoryYc3","HitTrajectoryYc4","HitTrajectoryYc5","HitTrajectoryYc6",
                                                        "HitTrajectoryYc7","ThrowSpeed","HitTrajectoryYc8","HitTrajectoryZc0","HitTrajectoryZc1","HitTrajectoryZc2","HitTrajectoryZc3","HitTrajectoryZc4","HitTrajectoryZc5","HitTrajectoryZc6","HitTrajectoryZc7","HitTrajectoryZc8",
                                                        "PopTime","ExchangeTime","TimeToBase","CatchPositionX","CatchPositionY","CatchPositionZ","ThrowPositionX","ThrowPositionY","ThrowPositionZ","BasePositionX","BasePositionY","BasePositionZ","ThrowTrajectoryXc0","ThrowTrajectoryXc1",
                                                        "ThrowTrajectoryXc2","ThrowTrajectoryYc0","ThrowTrajectoryYc1","ThrowTrajectoryYc2","ThrowTrajectoryZc0","ThrowTrajectoryZc1","ThrowTrajectoryZc2","PitchReleaseConfidence","PitchLocationConfidence","PitchMovementConfidence",
                                                        "HitLaunchConfidence","HitLandingConfidence",
                                                        "CatcherThrowCatchConfidence","CatcherThrowReleaseConfidence","CatcherThrowLocationConfidence"])
new=[]
listing=[]
for j in pitchers.index:
    dfs_list=[]
    for i in analysis_selection:
        df=pd.DataFrame(full_df.groupby(["Pitcher","TaggedPitchType"])[f'{i}'].mean().round(1))
        dfs_list=dfs_list+[df.loc[f'{j}']]
    now=pd.concat(dfs_list,axis=1)
    now_df=pd.DataFrame(now)
    now_df["Pitcher"]=j
    now_df.reset_index(inplace=True)
    new=new+[now_df]
finals=pd.concat(new,axis=0)
finals.set_index("Pitcher",inplace=True)
yes=finals.dropna()


yes_2=yes.drop(columns=["TaggedPitchType"])
grouped=yes_2.groupby("Pitcher").mean()

whiffs=all_pitches.loc[all_pitches["PitchCall"]=="StrikeSwinging"]
whiffs_df=pd.DataFrame(whiffs)
swings=all_pitches.loc[(all_pitches["PitchCall"]=="StrikeSwinging") | 
                       (all_pitches["PitchCall"]=="InPlay")|
                       (all_pitches["PitchCall"]=="FoulBallNotFieldable")|
                       (all_pitches["PitchCall"]=="FoulBallFieldable")]
swings_df=pd.DataFrame(swings)
number=len(whiffs_df)/len(swings)



hard_hit=all_pitches.loc[all_pitches["ExitSpeed"]>95]
hard_hit_df=pd.DataFrame(hard_hit)
in_play=all_pitches.loc[all_pitches["PitchCall"]=="InPlay"]
in_play_df=pd.DataFrame(in_play)
hard_hit_rate=len(hard_hit_df)/len(in_play_df)

ground=all_pitches.loc[all_pitches["Angle"]<10]
ground_df=pd.DataFrame(ground)
in_play=all_pitches.loc[all_pitches["PitchCall"]=="InPlay"]
in_play_df=pd.DataFrame(in_play)
ground_rate=len(ground_df)/len(in_play_df)

first=all_pitches.loc[(all_pitches["Balls"]==0)&(all_pitches["Strikes"]==0)]
first_df=pd.DataFrame(first)
first_df_2=first_df.loc[(all_pitches["PitchCall"]=="StrikeCalled")|
                        (all_pitches["PitchCall"]=="StrikeSwinging")|
                        (all_pitches["PitchCall"]=="InPlay")|
                        (all_pitches["PitchCall"]=="FoulBallNotFieldable")|
                        (all_pitches["PitchCall"]=="FoulBallFieldable")]
first_pitch=len(first_df_2)/len(first_df)



advanced=pd.DataFrame({"Statistic":["Whiff Rate","Hard Hit Rate","Ground Ball Rate","First Pitch Strike Rate"],
                       "Value":[number,hard_hit_rate,ground_rate,first_pitch]})

more_stats=st.checkbox("See Advanced Statistics")
if more_stats:
    st.write(advanced)

#First PCA
Principal=st.checkbox(f"Perform PCA on {pick_team} Pitchers")
if Principal:
    by_pitcher=st.selectbox("Pick an Analysis",["PCA by Pitcher","PCA by Pitches"])
    if by_pitcher=="PCA by Pitcher":
        
        hand=st.checkbox("Use absolute values")
        if hand:
           grouped_drop=grouped.dropna()
           grouped_drop=grouped_drop.abs()
           scaler= StandardScaler() 
           scaled_data=scaler.fit_transform(grouped_drop)
           pca=PCA() 
           scores=pca.fit_transform(scaled_data) 
           scaled_df=pd.DataFrame(scaled_data) 


           var=pca.explained_variance_ratio_ 
           variance_df = pd.DataFrame({'Variance': var }) 
           variance_df.index = [f'{i+1}' for i in range(len(var))] 
           scree=sns.barplot(x=variance_df.index,y=variance_df["Variance"],data=variance_df) 
           plt.xlabel("Principal Component") 
           plt.ylabel("Variance Explained") 
           plt.title("Scree Plot") 
           
           

           

            

           scores_df=pd.DataFrame(scores,columns=[f'PC{i+1}'for i in range(scores.shape[1])]) 

           scores_plot=px.scatter(scores_df,x="PC1",y="PC2")
           scores_df.index=grouped.index

           scores_df["Pitcher"]=grouped.index
           scores_df.index=scores_df["Pitcher"]
           scores_df.drop(columns=["Pitcher"],inplace=True)
           with_pitcher=scores_df.groupby("Pitcher").mean()
           with_pitcher["Name"]=with_pitcher.index

           scores_df=pd.DataFrame(with_pitcher) 
           scores_plot_2=px.scatter(scores_df,x="PC1",y="PC2",color="Name")
           scores_plot_2.update_traces(marker_size=10)
           scores_plot_2.update_xaxes(range=[-4,4])
           scores_plot_2.update_yaxes(range=[-3,3])


           st.write(scores_plot_2)
           st.pyplot(scree.figure)
           loadings_df=pd.DataFrame(pca.components_.T,columns=[f'PC{i+1}'for i in range(scores.shape[1])])
           things=pd.DataFrame({'PC':['RelSpeed','SpinRate','SpinAxis','InducedVertBreak',
                                                                   'HorzBreak','Extension',"VertApprAngle","HorzApprAngle"] })
           things_2=pd.merge(loadings_df,things,left_index=True,right_index=True)
           things_2.index=things_2["PC"]
           things_2.drop(columns="PC",inplace=True)
           things_2.reset_index(inplace=True)
           st.write("Loadings")
           st.write(things_2)
        

        if not hand:
            grouped_drop=grouped.dropna()
            scaler= StandardScaler() 
            scaled_data=scaler.fit_transform(grouped_drop)
            pca=PCA() 
            scores=pca.fit_transform(scaled_data) 
            scaled_df=pd.DataFrame(scaled_data) 


            var=pca.explained_variance_ratio_ 
            variance_df = pd.DataFrame({'Variance': var }) 
            variance_df.index = [f'{i+1}' for i in range(len(var))] 
            scree=sns.barplot(x=variance_df.index,y=variance_df["Variance"],data=variance_df) 
            plt.xlabel("Principal Component") 
            plt.ylabel("Variance Explained") 
            plt.title("Scree Plot") 

            

            scores_df=pd.DataFrame(scores,columns=[f'PC{i+1}'for i in range(scores.shape[1])]) 

            scores_plot=px.scatter(scores_df,x="PC1",y="PC2")
            scores_df.index=grouped.index

            scores_df["Pitcher"]=grouped.index
            scores_df.index=scores_df["Pitcher"]
            scores_df.drop(columns=["Pitcher"],inplace=True)
            with_pitcher=scores_df.groupby("Pitcher").mean()
            with_pitcher["Name"]=with_pitcher.index

            scores_df=pd.DataFrame(with_pitcher) 
            scores_plot_2=px.scatter(scores_df,x="PC1",y="PC2",color="Name")
            scores_plot_2.update_traces(marker_size=10)

            scores_plot_2.update_xaxes(range=[-4,4])
            scores_plot_2.update_yaxes(range=[-3,3])
            st.write(scores_plot_2)
            st.pyplot(scree.figure) 
            loadings_df=pd.DataFrame(pca.components_.T,columns=[f'PC{i+1}'for i in range(scores.shape[1])])
            things=pd.DataFrame({'PC':['RelSpeed','SpinRate','SpinAxis','InducedVertBreak',
                                                                   'HorzBreak','Extension',"VertApprAngle","HorzApprAngle"] })
            things_2=pd.merge(loadings_df,things,left_index=True,right_index=True)
            things_2.index=things_2["PC"]
            things_2.drop(columns="PC",inplace=True)
            things_2.reset_index(inplace=True)
            st.write("Loadings")
            st.write(things_2)







    


    if by_pitcher=="PCA by Pitches":
        hand=st.checkbox("Use absolute values")
        if hand:
            full_df_drop=full_df_drop.dropna()
            finals_drop=finals.dropna()
            finals_drop_here=finals_drop.drop(columns=["TaggedPitchType"])
            finals_drop_here=finals_drop_here.abs()
            scaler= StandardScaler() 
            scaled_data=scaler.fit_transform(finals_drop_here)
            pca=PCA() 
            scores=pca.fit_transform(scaled_data) 
            scaled_df=pd.DataFrame(scaled_data) 


            plt.clf()
            var=pca.explained_variance_ratio_ 
            variance_df = pd.DataFrame({'Variance': var }) 
            variance_df.index = [f'{i+1}' for i in range(len(var))] 
            scree_3=sns.barplot(x=variance_df.index,y=variance_df["Variance"],data=variance_df) 
            plt.xlabel("Principal Component") 
            plt.ylabel("Variance Explained") 
            plt.title("Scree Plot") 


        


            scores_df=pd.DataFrame(scores,columns=[f'PC{i+1}'for i in range(scores.shape[1])]) 

            pitch_type_df=pd.DataFrame(finals_drop["TaggedPitchType"])
            pitch_type_df.reset_index(inplace=True)


            together=pd.concat([scores_df,pitch_type_df],axis=1)



            scores_plot=px.scatter(together,x="PC1",y="PC2",color="TaggedPitchType",hover_data=["Pitcher"])
            scores_df.index=finals_drop.index
            scores_plot.update_traces(marker_size=7)

            scores_plot.update_xaxes(range=[-4,4])
            scores_plot.update_yaxes(range=[-3,3])
            st.write(scores_plot)
            st.pyplot(scree_3.figure)
            loadings_df=pd.DataFrame(pca.components_.T,columns=[f'PC{i+1}'for i in range(scores.shape[1])])
            things=pd.DataFrame({'PC':['RelSpeed','SpinRate','SpinAxis','InducedVertBreak',
                                                                   'HorzBreak','Extension',"VertApprAngle","HorzApprAngle"] })
            things_2=pd.merge(loadings_df,things,left_index=True,right_index=True)
            things_2.index=things_2["PC"]
            things_2.drop(columns="PC",inplace=True)
            things_2.reset_index(inplace=True)
            st.write("Loadings")
            st.write(things_2) 

        if not hand:
            full_df_drop=full_df_drop.dropna()
            finals_drop=finals.dropna()
            finals_drop_here=finals_drop.drop(columns=["TaggedPitchType"])
            scaler= StandardScaler() 
            scaled_data=scaler.fit_transform(finals_drop_here)
            pca=PCA() 
            scores=pca.fit_transform(scaled_data) 
            scaled_df=pd.DataFrame(scaled_data) 


            plt.clf()
            var=pca.explained_variance_ratio_ 
            variance_df = pd.DataFrame({'Variance': var }) 
            variance_df.index = [f'{i+1}' for i in range(len(var))] 
            scree_2=sns.barplot(x=variance_df.index,y=variance_df["Variance"],data=variance_df) 
            plt.xlabel("Principal Component") 
            plt.ylabel("Variance Explained") 
            plt.title("Scree Plot") 


        


            scores_df=pd.DataFrame(scores,columns=[f'PC{i+1}'for i in range(scores.shape[1])]) 

            pitch_type_df=pd.DataFrame(finals_drop["TaggedPitchType"])
            pitch_type_df.reset_index(inplace=True)


            together=pd.concat([scores_df,pitch_type_df],axis=1)



            scores_plot=px.scatter(together,x="PC1",y="PC2",color="TaggedPitchType",hover_data=["Pitcher"])
            scores_df.index=finals_drop.index
            scores_plot.update_traces(marker_size=7)

            scores_plot.update_xaxes(range=[-4,4])
            scores_plot.update_yaxes(range=[-3,3])
            st.write(scores_plot)
            st.pyplot(scree_2.figure)
            loadings_df=pd.DataFrame(pca.components_.T,columns=[f'PC{i+1}'for i in range(scores.shape[1])])
            things=pd.DataFrame({'PC':['RelSpeed','SpinRate','SpinAxis','InducedVertBreak',
                                                                   'HorzBreak','Extension',"VertApprAngle","HorzApprAngle"] })
            things_2=pd.merge(loadings_df,things,left_index=True,right_index=True)
            things_2.index=things_2["PC"]
            things_2.drop(columns="PC",inplace=True)
            things_2.reset_index(inplace=True)
            st.write("Loadings")
            st.write(things_2) 



