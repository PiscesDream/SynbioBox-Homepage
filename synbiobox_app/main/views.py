from flask import render_template, jsonify, request, current_app, send_file, abort, url_for, redirect
from datetime import datetime
import cPickle
from .. import app 


rec_file = 'synbiobox_app/record.txt'
download_dict = { 'Android (4.2 at least)': ['v1.92', 'Android (4.2 at least).zip','2d18b348ef1af93e5c489a9df5d4b434', 0, 1],
                  'BlackBerry'            : ['v1.92', 'BlackBerry.zip'            ,'46293624a7d8ac58788bb9891e6c2cfb', 0, 0],
                  'Linux x86'             : ['v1.92', 'Linux x86.zip'             ,'01ead043c0dd682f323b019368ed8fd0', 0, 0],
                  'Linux x86_64'          : ['v1.92', 'Linux x86_64.zip'          ,'36509b5319fa3ab371e12710d6688ead', 0, 0],
                  'Mac OS x x86'          : ['v1.92', 'Mac OS x x86.zip'          ,'28ef1a087294790d625efc3ed310e4f4', 0, 0],
                  'Mac OS x x86_64'       : ['v1.92', 'Mac OS x x86_64.zip'       ,'6677d66a516477142a514eb237b76f0f', 0, 0],
                  'Samsung TV'            : ['v1.92', 'Samsung TV.zip'            ,'fec3235d511c43e09305dd6d62e24e8c', 0, 0],
                  'Windows x86'           : ['v1.92', 'Windows x86.zip'           ,'78035e6e6509c25110daf370716e4569', 0, 1],
                  'Windows x86_64'        : ['v1.92', 'Windows x86_64.zip'        ,'28801ebc4135d88e9074b80371b6d7f8', 0, 1],
                  'Web player'            : ['v1.92', ''                          ,''                                , 0, 1]}

@app.route('/')
def index():
    with open(rec_file, 'rb') as f:
        rec = cPickle.load(f)
    for platform, info in download_dict.iteritems():
        info[3] = len(rec.get(platform, []))

    return render_template('index.html', download_dict=iter(sorted(download_dict.iteritems())))

@app.route('/link/<platform>')
def link(platform):
    platform=platform.strip()

    if 1:
        with open(rec_file, 'rb') as f:
            rec = cPickle.load(f)

        if rec.has_key(platform):
            rec[platform].append( (request.remote_addr,  datetime.now().strftime('%Y-%m-%d %H:%M:%S')) )
        else:
            rec[platform] = [(request.remote_addr,  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]

        with open(rec_file, 'wb') as f:
            cPickle.dump(rec, f)

        download_dict[platform][3] += 1

        if platform == 'Web player':
            return redirect('http://online.synbiobox.hapd.info')
        else:
            return send_file('file/'+download_dict[platform][1])
    else:
        abort(404)
        



