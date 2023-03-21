from django.shortcuts import render, redirect
from django.db.models import Count, Avg, Max, Min, Sum
from home import models
import os
from sweeper_command.settings import BASE_DIR
import folium
import pandas as pd
import datetime
import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from home import CGNet
import time
# Create your views here.
class Detection():
    def __init__(self) -> None:
        self.seg_model = CGNet.CGNet(classes=4)
    def cuda_detect(self,cuda,gpus):
        if cuda:
            device = torch.device("cuda")
            os.environ["CUDA_VISIBLE_DEVICES"] = gpus
            if not torch.cuda.is_available():
                raise Exception("no GPU found or wrong gpu id, please run without --cuda")
        else:
            device = torch.device("cpu")
        return device
    
    def model_evaluation(self,model,checkpoint_path,device):
        cudnn.benchmark = True
        if checkpoint_path:
            if os.path.isfile(checkpoint_path):
                checkpoint = torch.load(checkpoint_path, map_location=device)
                model.load_state_dict(checkpoint['model'])
            else:
                raise FileNotFoundError("no checkpoint found at '{}'".format(checkpoint_path))
        return model

    def image_augmentation(self,predict_image):
        image = cv2.cvtColor(predict_image, cv2.IMREAD_COLOR)
        dim = (480,360)
        mean=(89.02598,91.51838,91.355064) #(115.20707,115.52273,115.017975) #mean=(117.64809,123.275635,124.548775)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        image = np.asarray(image, np.float32)
        image -= mean
        image = image[:, :, ::-1]  # revert to RGB
        image = image.transpose((2, 0, 1))  # HWC -> CHW
        output_image = image.copy()
        output_image = torch.from_numpy(output_image).unsqueeze(0)
        return output_image  
    def cal_unclean_degree(self, seg_output):
        output = seg_output.cpu().data[0].numpy()
        output = output.transpose(1, 2, 0)
        output = np.asarray(np.argmax(output, axis=2), dtype=np.uint8)
        label_output = output.copy()
        return label_output
    def avi_to_web_mp4(self, input_file_path, output_file_path):
        cmd = 'ffmpeg -y -i {} -vcodec h264 {}'.format(input_file_path, output_file_path)
        os.system(cmd)
    def predict_video(self, savevideopath, vehicle_id, currentdate, currenttime, fourcc, fps, size, cuda = True, gpus = "0", checkpoint_path = ''):
        device = self.cuda_detect(cuda,gpus)
        model = self.model_evaluation(self.seg_model,checkpoint_path,device)
        if not os.path.exists(savevideopath):
            print('video is not exist!')
            return 0
        capture = cv2.VideoCapture(savevideopath)
        if not capture.isOpened():
            print('==========> please check your video name')
            return 0
        
        processvideo = os.path.join(BASE_DIR,"home","static","home","data",vehicle_id + '_' + currentdate+'-'+currenttime + '.avi')
        videoWriter = cv2.VideoWriter(processvideo,fourcc,fps,size)
        #videoWriter.open(processvideo,fourcc,fps,size,True)
        while capture.isOpened():           
            ret,predict_image=capture.read() # img 就是一帧图片
            count = 0
            if ret:
                # image = CvBridge().imgmsg_to_cv2(predict_image)              
                image = self.image_augmentation(predict_image)
                model.eval()
                model = model.to(device)
                with torch.no_grad():
                    input_var = image.to(device)
                seg_output = model(input_var)
                label_output = self.cal_unclean_degree(seg_output)
                predict_image = cv2.resize(predict_image,(480,360), interpolation=cv2.INTER_LINEAR)
                # if rate_trash_road >= 0.05 and count % 10 == 0:
                if count % 10 == 0:
                    _,thresh = cv2.threshold(label_output,2,255,cv2.THRESH_BINARY)
                    _, contours, _= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # ! opencv version is 3.4.1.15, not opencv4
                    # contours=np.asarray(contours)
                    # print(type(contours))
                    # predict_image = cv2.resize(predict_image,(480,360), interpolation=cv2.INTER_LINEAR)
                    cv2.drawContours(predict_image,contours,-1,(0,0,255),2)
                    try:
                        predict_image = cv2.resize(predict_image, (800,600), interpolation=cv2.INTER_LINEAR)
                        videoWriter.write(predict_image)
                    except KeyboardInterrupt:
                        raise        
                    except Exception:
                        pass
                count += 1         
            else:
                break # 当获取完最后一帧就结束
        capture.release()
        videoWriter.release()
        avivideopath = os.path.join(BASE_DIR,"home","static","home","data",vehicle_id + '_' + currentdate+'-'+currenttime + '.avi')
        outputvideopath = os.path.join(BASE_DIR,"home","static","home","data",vehicle_id + '_' + currentdate+'-'+currenttime + 'detected.mp4')
        self.avi_to_web_mp4(avivideopath,outputvideopath)
        return processvideo


def index(request):
    today_time = datetime.date.today().strftime('%m-%d-%Y')
    # today_time = '11-04-2022'
    total = models.Total.objects.all()
    total_today = models.Total.objects.all().filter(currentdate=today_time)
    state_dict = {'Western Water Catchment':['WC',52],'Jurong East':['JE',8],'Unknown':['WC',52]}
    state_unclean = f"./home/static/home/foliumdata/SG_dis_data.csv"
    state_geo = f"./home/static/home/foliumdata/sg-districts.json"
    state_data = pd.read_csv(state_unclean)
    currentsuburb_list = list(total_today.values("suburb").annotate(count=Count("suburb")).annotate(count=Sum('avg_unclean_level')))
    for currentsuburb in currentsuburb_list:
        state_data.loc[state_dict[currentsuburb['suburb']][1],'Unclean']=float(currentsuburb['count'])
    choro_m = folium.Map(location=[1.36579,103.83433], zoom_start=12) 
    folium.Choropleth(
        geo_data=state_geo,
        name="choropleth",
        data=state_data,
        columns=["State", "Unclean"],
        key_on="feature.id",
        fill_color="OrRd",
        fill_opacity=0.4,
        line_opacity=0.7,
        legend_name="Unclean Rate (%)",
    ).add_to(choro_m)
    folium.LayerControl().add_to(choro_m)
    choro_m.save("./home/static/home/foliumdata/choro.html")
    return render(request, "index.html", {'total':total})

def index_normal(request):
    total = models.Total.objects.all()
    return render(request, "index_normal.html", {'total':total})

def charts(request):
    # print(total.filter(pub_date__year=2022))
    reports = models.Total.objects.values("currentdate").annotate(road=Max('road'), suburb = Max('suburb'), county = Max('county'),start_time=Min('currenttime'),end_time=Max('currenttime'))
    return render(request, "charts.html", {'reports':reports})

def generate_report(request):
    currentdate = request.GET.get('currentdate')
    report_map_name = os.path.join(BASE_DIR,"home","static","home","data",'reportmap_' + currentdate + '.html')
    report_map_path = '/home/data/' + 'reportmap_' + currentdate + '.html'
    objects = models.Total.objects.filter(currentdate=currentdate)
    current_location = folium.Map(location=[1.36579,103.83433], zoom_start=12) 
    for object in objects:
        gps = [float(object.latitude), float(object.longitude)]
        folium.Marker(
        gps, popup=object.vehicle_id).add_to(current_location)
    current_location.save(report_map_name)

    suburb_list = list(objects.values('suburb').annotate(avg_level=Avg('avg_unclean_level') * Avg('duration')).values_list('suburb',flat=True))
    suburb_index_list = list(objects.values('suburb').annotate(avg_level=Avg('avg_unclean_level') * Avg('duration')).values_list('avg_level',flat=True))
    bar_info = '''
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';

    var ctx = document.getElementById("myBarChart");
    var myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ''' + str(suburb_list) + ''',
        datasets: [{
        label: "Unclean_Index",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
        data: ''' + str(suburb_index_list) + ''',
        }],
    },
    options: {
        scales: {
        xAxes: [{
            time: {
            unit: 'month'
            },
            gridLines: {
            display: false
            },
            ticks: {
            maxTicksLimit: 6
            }
        }],
        yAxes: [{
            ticks: {
            min: 0,
            max: 100,
            maxTicksLimit: 5
            },
            gridLines: {
            display: true
            }
        }],
        },
        legend: {
        display: false
        }
    }
    });
    '''
    bar_js = os.path.join(BASE_DIR, "home", "static", "home", "data", "chart-bar_" + currentdate + ".js")
    bar_js_path = '/home/data/chart-bar_' + currentdate + '.js'
    bar_js_file = open(bar_js,'w')
    bar_js_file.write(bar_info)
    bar_js_file.close()

    vehicle_id_list = list(objects.values('vehicle_id').annotate(count=Count('vehicle_id')).values_list('vehicle_id',flat=True))
    vehicle_count_list = list(objects.values('vehicle_id').annotate(count=Count('vehicle_id')).values_list('count',flat=True))
    pie_info = '''
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';
    var ctx = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ''' + str(vehicle_id_list) + ''',
        datasets: [{
        data: ''' + str(vehicle_count_list) + ''',
        backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745', '#123213'],
        }],
    },
    });
    '''
    pie_js = os.path.join(BASE_DIR, "home", "static", "home", "data", "chart-pie_" + currentdate + ".js")
    pie_js_path = '/home/data/chart-pie_' + currentdate + '.js'
    pie_js_file = open(pie_js,'w')
    pie_js_file.write(pie_info)
    pie_js_file.close()

    message = ''' 
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
            <meta name="description" content="" />
            <meta name="author" content="" />
            <title>Reports - Sweeper Audit</title>
            <link href="{% static '/home/css/styles.css' %}" rel="stylesheet" type="text/css" />
            <script src="https://use.fontawesome.com/releases/v6.1.0/js/all.js" crossorigin="anonymous"></script>
        </head>
        <body class="sb-nav-fixed bg-dark">
            <nav class="sb-topnav navbar navbar-expand navbar-dark bg-dark">
                <!-- Navbar Brand-->
                <a class="navbar-brand ps-3"><img src="{% static "/home/NTU_Logo.png" %}" class="img-fluid"></a>
                <!-- Sidebar Toggle-->
                <button class="btn btn-link btn-lg order-1 order-lg-0 me-4 me-lg-0" id="sidebarToggle" href="#!"><i class="fas fa-bars"></i></button>
                <a class="navbar-title ps-5" href="{% url 'index' %}">Sweeper Audit System</a>
                <!-- Navbar-->
                <ul class="d-none d-md-inline-block form-inline ms-auto me-0 me-md-3 my-2 my-md-0">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" id="navbarDropdown" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"><i class="fas fa-user fa-fw"></i></a>
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                            <li><a class="dropdown-item" href="#!">Settings</a></li>
                            <li><hr class="dropdown-divider" /></li>
                            <li><a class="dropdown-item" href="{% url 'login' %}">Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </nav>
            <div id="layoutSidenav">
                <div id="layoutSidenav_nav">
                    <nav class="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
                        <div class="sb-sidenav-menu">
                            <div class="nav">
                                <div class="sb-sidenav-menu-heading">Core</div>
                                <a class="nav-link" href="{% url 'index' %}">
                                    <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                    Dashboard
                                </a>
                                <div class="sb-sidenav-menu-heading">Addons</div>
                                <a class="nav-link" href="{% url 'charts' %}">
                                    <div class="sb-nav-link-icon"><i class="fas fa-chart-area"></i></div>
                                    Reports
                                </a>
                                <a class="nav-link" href="{% url 'tables' %}">
                                    <div class="sb-nav-link-icon"><i class="fas fa-table"></i></div>
                                    Tables
                                </a>
                            </div>
                        </div>
                        <div class="sb-sidenav-footer">
                            <div class="small">Logged in as:</div>
                            NTU
                        </div>
                    </nav>
                </div>
                <div id="layoutSidenav_content">
                    <main>
                        <div class="container-fluid px-4 bg-secondary my-4">
                            <h1 class="mt-5 mb-2">Reports</h1>
                            <ol class="breadcrumb mb-3">
                                <li class="breadcrumb-item"><a href="">Dashboard</a></li>
                                <li class="breadcrumb-item active">Reports</li>
                            </ol>
                            <div class="row">
                                <div class="col-lg-6">
                                    <div class="card mb-4">
                                        <div class="card-header">
                                            <i class="fas fa-chart-bar me-1"></i>
                                            Unclean Index for each suburb
                                        </div>
                                        <div class="card-body"><canvas id="myBarChart" width="100%" height="50"></canvas></div>
                                        <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>
                                    </div>
                                </div>
                                <div class="col-lg-6">
                                    <div class="card mb-4">
                                        <div class="card-header">
                                            <i class="fas fa-chart-pie me-1"></i>
                                            Unclean detected times for each vehicle
                                        </div>
                                        <div class="card-body"><canvas id="myPieChart" width="100%" height="50"></canvas></div>
                                        <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>
                                    </div>
                                </div>
                            </div>
                            <div class="card mb-4">
                                <div class="card-header">
                                    <i class="fas fa-chart-area me-1"></i>
                                    Area Chart Example
                                </div>
                                <div style="position:relative;width:100%;height:1;padding-bottom:40%;">
                                    <iframe src="{% static "''' + report_map_path + '''" %}" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;"></iframe>
                                </div>
                                <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>
                            </div>
                        </div>
                    </main>
                    <footer class="py-4 bg-secondary">
                        <div class="container-fluid px-4">
                            <div class="d-flex align-items-center justify-content-between small">
                                <div class="text-white">Copyright &copy; Your Website 2022</div>
                                <div>
                                    <a href="#">Privacy Policy</a>
                                    &middot;
                                    <a href="#">Terms &amp; Conditions</a>
                                </div>
                            </div>
                        </div>
                    </footer>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
            <script src="{% static '/home/js/scripts.js' %}"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js" crossorigin="anonymous"></script>
            <script src="{% static "''' + bar_js_path + '''" %}"></script>
            <script src="{% static "''' + pie_js_path + '''" %}"></script>
        </body>
    </html>
    '''
    html_name = os.path.join(BASE_DIR,"home", "templates", "detail", 'report_' + currentdate + '.html')
    html_file = open(html_name,'w')
    html_file.write(message)
    html_file.close()
    return render(request, 'detail/' + 'report_' + currentdate + '.html')

def drop_report(request):
    drop_currentdate = request.GET.get('currentdate')
    if os.path.exists(BASE_DIR+'/home/static/home/data/chart-pie_'+drop_currentdate+'.js'):
        os.remove(BASE_DIR+'/home/static/home/data/chart-pie_'+drop_currentdate+'.js')
    if os.path.exists(BASE_DIR+'/home/static/home/data/chart-bar_'+drop_currentdate+'.js'):
        os.remove(BASE_DIR+'/home/static/home/data/chart-bar_'+drop_currentdate+'.js')
    if os.path.exists(BASE_DIR+'/home/static/home/data/reportmap_'+drop_currentdate+'.html'):
        os.remove(BASE_DIR+'/home/static/home/data/reportmap_'+drop_currentdate+'.html')   
    if os.path.exists(BASE_DIR+'/home/templates/detail/report_'+drop_currentdate+'.html'):
        os.remove(BASE_DIR+'/home/templates/detail/report_'+drop_currentdate+'.html')
    return redirect('charts')


def charts_normal(request):
    return render(request, "charts_normal.html")

def tables(request):
    total = models.Total.objects.all()
    return render(request, "tables.html", {'total':total})

def tables_normal(request):
    total = models.Total.objects.all()
    return render(request, "tables_normal.html", {'total':total})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'ntu' and password == 'ntu':
            return redirect('index')
        else:
            return redirect('index_normal')
    return render(request, "login.html")

def drop_info_index(request):
    drop_id = request.GET.get('id')
    drop_obj = models.Total.objects.get(id=drop_id)
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.mp4'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.mp4')
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'detected.mp4'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'detected.mp4')
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.avi'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.avi')
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.png'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.png')    
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'_map.html'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'_map.html') 
    if os.path.exists(BASE_DIR+'/home/templates/detail/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.html'):
        os.remove(BASE_DIR+'/home/templates/detail/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.html')   
    drop_obj.delete()
    return redirect('index')

def drop_info_tables(request):
    drop_id = request.GET.get('id')
    drop_obj = models.Total.objects.get(id=drop_id)
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.mp4'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.mp4')
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'detected.mp4'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'detected.mp4')
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.avi'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.avi')
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.png'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.png')    
    if os.path.exists(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'_map.html'):
        os.remove(BASE_DIR+'/home/static/home/data/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'_map.html') 
    if os.path.exists(BASE_DIR+'/home/templates/detail/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.html'):
        os.remove(BASE_DIR+'/home/templates/detail/'+drop_obj.vehicle_id+'_'+drop_obj.currentdate+'-'+drop_obj.currenttime+'.html') 

    drop_obj.delete()
    return redirect('tables')

def generate_new_detail_info(request):
    vehicle_id = request.GET.get('vehicle_id')
    company = request.GET.get('company')
    currentdate = request.GET.get('currentdate')
    currenttime = request.GET.get('currenttime')
    road = request.GET.get('road')
    suburb = request.GET.get('suburb')
    county = request.GET.get('county')
    postcode = request.GET.get('postcode')
    avg_unclean_level = request.GET.get('avg_unclean_level')
    duration = request.GET.get('duration')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    html_name = os.path.join(BASE_DIR,"home","templates","detail",vehicle_id + '_' + currentdate+'-'+currenttime + '.html')
    map_name = os.path.join(BASE_DIR,"home","static","home","data",vehicle_id + '_' + currentdate+'-'+currenttime + '_map.html')
    png_path = '/home/data/' + vehicle_id + '_' + currentdate+'-'+currenttime + '.png'
    mp4_path = '/home/data/' + vehicle_id + '_' + currentdate+'-'+currenttime + 'detected.mp4'
    map_path = '/home/data/' + vehicle_id + '_' + currentdate+'-'+currenttime + '_map.html'
    save_mp4_name = os.path.join(BASE_DIR,"home","static","home","data",vehicle_id + '_' + currentdate+'-'+currenttime + '.mp4')
    T1 = time.time()
    Detection().predict_video(savevideopath=save_mp4_name, vehicle_id=vehicle_id, currentdate=currentdate, currenttime=currenttime ,fourcc=cv2.VideoWriter_fourcc(*'XVID'), fps = 20 ,size=(800,600), cuda = True, gpus = "0",checkpoint_path =r'C:/Users/NTU-NUC2/sweeper_audit/environment_configuration/command_center/sweeper_command_center/home/CGNET_model_291.pth')
    T2 = time.time()
    print('-----------------------------------detection time is %ss-----------------------------------' % (T2 - T1))
    gps = [float(latitude), float(longitude)]
    current_location = folium.Map(location=gps, zoom_start=30) 
    folium.Marker(
    gps, popup="Sweeper", tooltip=str(road) + ', ' + str(suburb) + ', ' + str(county) + ', ' + str(postcode)
    ).add_to(current_location)
    current_location.save(map_name)
    message = '''
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
            <meta name="description" content="" />
            <meta name="author" content="" />
            <title>Reports - Sweeper Audit</title>
            <link href="{% static '/home/css/styles.css' %}" rel="stylesheet" type="text/css" />
            <script src="https://use.fontawesome.com/releases/v6.1.0/js/all.js" crossorigin="anonymous"></script>
        </head>
        <body class="sb-nav-fixed bg-dark">
            <nav class="sb-topnav navbar navbar-expand navbar-dark bg-dark">
                <!-- Navbar Brand-->
                <a class="navbar-brand ps-3"><img src="{% static "/home/NTU_Logo.png" %}" class="img-fluid"></a>
                <!-- Sidebar Toggle-->
                <button class="btn btn-link btn-lg order-1 order-lg-0 me-4 me-lg-0" id="sidebarToggle" href="#!"><i class="fas fa-bars"></i></button>
                <a class="navbar-title ps-5" href="{% url 'index' %}">Sweeper Audit System</a>
                <!-- Navbar-->
                <ul class="d-none d-md-inline-block form-inline ms-auto me-0 me-md-3 my-2 my-md-0">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" id="navbarDropdown" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"><i class="fas fa-user fa-fw"></i></a>
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                            <li><a class="dropdown-item" href="#!">Settings</a></li>
                            <li><hr class="dropdown-divider" /></li>
                            <li><a class="dropdown-item" href="{% url 'login' %}">Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </nav>
            <div id="layoutSidenav">
                <div id="layoutSidenav_nav">
                    <nav class="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
                        <div class="sb-sidenav-menu">
                            <div class="nav">
                                <div class="sb-sidenav-menu-heading">Core</div>
                                <a class="nav-link" href="{% url 'index' %}">
                                    <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                    Dashboard
                                </a>
                                <div class="sb-sidenav-menu-heading">Addons</div>
                                <a class="nav-link" href="{% url 'charts' %}">
                                    <div class="sb-nav-link-icon"><i class="fas fa-chart-area"></i></div>
                                    Reports
                                </a>
                                <a class="nav-link" href="{% url 'tables' %}">
                                    <div class="sb-nav-link-icon"><i class="fas fa-table"></i></div>
                                    Tables
                                </a>
                            </div>
                        </div>
                        <div class="sb-sidenav-footer">
                            <div class="small">Logged in as:</div>
                            NTU
                        </div>
                    </nav>
                </div>
                <div id="layoutSidenav_content">
                    <main>
                        <div class="container-fluid px-4 bg-secondary my-4">
                            <h1 class="mt-5 mb-2">Reports</h1>
                            <ol class="breadcrumb mb-3">
                                <li class="breadcrumb-item"><a href="">Dashboard</a></li>
                                <li class="breadcrumb-item active">Reports</li>
                            </ol>
                            <div class="card mb-4">
                                <div class="card-header">
                                    <i class="fas fa-chart-area me-1"></i>
                                    Area Chart Example
                                </div>
                                <div class="card-body">
                                    <table id="datatablesSimple">
                                        <thead>
                                            <tr>
                                                <th>VehicleID</th>
                                                <th>Company</th>
                                                <th>Currentdate</th>
                                                <th>Currenttime</th>
                                                <th>Road</th>
                                                <th>Suburb</th>
                                                <th>County</th>
                                                <th>Postcode</th>
                                                <th>Level</th>
                                                <th>Duration(sec)</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>'''+ str(vehicle_id) + '''</td>
                                                <td>'''+ str(company) + '''</td>
                                                <td>'''+ str(currentdate) + '''</td>
                                                <td>'''+ str(currenttime) + '''</td>
                                                <td>'''+ str(road) + '''</td>
                                                <td>'''+ str(suburb) + '''</td>
                                                <td>'''+ str(county) + '''</td>
                                                <td>'''+ str(postcode) + '''</td>
                                                <td>'''+ str(avg_unclean_level) + '''</td>
                                                <td>'''+ str(duration) + '''</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <!-- <div class="card-body"><canvas id="myAreaChart" width="100%" height="10"></canvas></div> -->
                                <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>
                            </div>
                            <div class="row">
                                <div class="col-lg-6">
                                    <div class="card mb-4">
                                        <div class="card-header">
                                            <i class="fas fa-chart-bar me-1"></i>
                                            Shown Image
                                        </div>
                                        <img src="{% static "''' + png_path + '''" %}" class="img-fluid">
                                        <div class="card-footer small text-muted">Updated</div>
                                    </div>
                                </div>
                                <div class="col-lg-6">
                                    <div class="card mb-4">
                                        <div class="card-header">
                                            <i class="fas fa-chart-pie me-1"></i>
                                            Map Location
                                        </div>
                                        <div style="position:relative;width:100%;height:1;padding-bottom:75%;">
                                            <iframe src="{% static "''' + map_path + '''" %}" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;"></iframe>
                                        </div>
                                        <div class="card-footer small text-muted">Updated</div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-6">
                                    <div class="card mb-4">
                                        <div class="card-header">
                                            <i class="fas fa-chart-pie me-1"></i>
                                            Shown Video
                                        </div>
                                        <div class="embed-responsive embed-responsive-16by9">
                                            <video controls>
                                            <source src="{% static "''' + mp4_path + '''" %}" type="video/mp4">
                                            </video>
                                            </div>
                                        <div class="card-footer small text-muted">Updated</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>
                    <footer class="py-4 bg-secondary">
                        <div class="container-fluid px-4">
                            <div class="d-flex align-items-center justify-content-between small">
                                <div class="text-white">Copyright &copy; Your Website 2022</div>
                                <div>
                                    <a href="#">Privacy Policy</a>
                                    &middot;
                                    <a href="#">Terms &amp; Conditions</a>
                                </div>
                            </div>
                        </div>
                    </footer>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
            <script src="{% static '/home/js/scripts.js' %}"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js" crossorigin="anonymous"></script>
            <script src="{% static '/home/assets/demo/chart-area-demo.js' %}"></script>
            <script src="{% static '/home/assets/demo/chart-bar-demo.js' %}"></script>
            <script src="{% static '/home/assets/demo/chart-pie-demo.js' %}"></script>
            <script src="https://cdn.jsdelivr.net/npm/simple-datatables@latest" crossorigin="anonymous"></script>
            <script src="{% static '/home/js/datatables-simple-demo.js' %}"></script>
        </body>
    </html>
    '''
    html_file = open(html_name,'w')
    html_file.write(message)
    html_file.close()
    return render(request, 'detail/' + vehicle_id + '_' + currentdate+'-'+currenttime + '.html')