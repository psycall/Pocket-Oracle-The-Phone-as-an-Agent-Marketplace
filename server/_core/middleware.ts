import { Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import winston from 'winston';

/**
 * Security and logging middleware for ORVION
 */

// Configure Winston logger
export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'orvion-api' },
  transports: [
    new winston.transports.File({ filename: '.manus-logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: '.manus-logs/combined.log' }),
  ],
});

// Add console transport in development
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    ),
  }));
}

/**
 * Helmet middleware for security headers
 */
export function getHelmetMiddleware() {
  return helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
        connectSrc: ["'self'", 'https:'],
      },
    },
    hsts: {
      maxAge: 31536000, // 1 year
      includeSubDomains: true,
      preload: true,
    },
  });
}

/**
 * Rate limiting middleware
 * Different limits for different endpoints
 */
export const createRateLimiter = (windowMs: number = 15 * 60 * 1000, max: number = 100) => {
  return rateLimit({
    windowMs,
    max,
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true, // Return rate limit info in `RateLimit-*` headers
    legacyHeaders: false, // Disable `X-RateLimit-*` headers
    skip: (req) => {
      // Skip rate limiting for health checks
      return req.path === '/health';
    },
  });
};

/**
 * API rate limiter (100 requests per 15 minutes)
 */
export const apiLimiter = createRateLimiter(15 * 60 * 1000, 100);

/**
 * Auth rate limiter (5 login attempts per 15 minutes)
 */
export const authLimiter = createRateLimiter(15 * 60 * 1000, 5);

/**
 * Settlement rate limiter (50 settlements per hour)
 */
export const settlementLimiter = createRateLimiter(60 * 60 * 1000, 50);

/**
 * Request logging middleware
 */
export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    const logData = {
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip,
      userAgent: req.get('user-agent'),
    };

    if (res.statusCode >= 400) {
      logger.warn('HTTP Request', logData);
    } else {
      logger.info('HTTP Request', logData);
    }
  });

  next();
}

/**
 * Error logging middleware
 */
export function errorLogger(err: Error, req: Request, res: Response, next: NextFunction) {
  logger.error('Unhandled Error', {
    message: err.message,
    stack: err.stack,
    method: req.method,
    path: req.path,
    ip: req.ip,
  });

  next(err);
}

/**
 * CORS configuration
 */
export const corsOptions = {
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 3600,
};

/**
 * Health check endpoint
 */
export function healthCheck(req: Request, res: Response) {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV,
  });
}

/**
 * Request validation middleware
 */
export function validateContentType(req: Request, res: Response, next: NextFunction) {
  if (['POST', 'PUT', 'PATCH'].includes(req.method)) {
    const contentType = req.get('content-type');
    if (!contentType?.includes('application/json')) {
      return res.status(400).json({
        error: 'Content-Type must be application/json',
      });
    }
  }
  next();
}

/**
 * Request size limiter
 */
export const requestSizeLimiter = (maxSize: string = '10mb') => {
  return (req: Request, res: Response, next: NextFunction) => {
    const contentLength = parseInt(req.get('content-length') || '0', 10);
    const maxBytes = parseInt(maxSize) * 1024 * 1024;

    if (contentLength > maxBytes) {
      return res.status(413).json({
        error: `Request body too large. Maximum size is ${maxSize}`,
      });
    }
    next();
  };
};

/**
 * Sanitize request data
 */
export function sanitizeRequest(req: Request, res: Response, next: NextFunction) {
  // Remove sensitive headers
  req.headers['authorization'] = req.headers['authorization']?.substring(0, 20) + '...';

  next();
}
