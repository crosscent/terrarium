backend gunicorn {
    .host = "127.0.0.1";
    .port = "8000";
}

sub vcl_recv {
    set req.backend = gunicorn;
    return (pass);
}

